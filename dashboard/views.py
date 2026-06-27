import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET

from .forms import VideoForm
from .models import Video, VideoStatus
from .services import VideoProcessingService
from .tasks import enqueue_video_processing

logger = logging.getLogger(__name__)


def _require_video_owner(request, video: Video) -> None:
    if video.uploaded_by != request.user:
        raise PermissionDenied("You do not have access to this video.")


@login_required(login_url="/accounts/login", redirect_field_name="")
def home(request):
    videos = Video.objects.filter(uploaded_by=request.user)
    return render(request, "dashboard/video_listings.html", {"uploaded_videos": videos})


@login_required(login_url="/accounts/login", redirect_field_name="")
def upload(request):
    form = VideoForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        video = form.save(commit=False)
        video.uploaded_by = request.user
        video.status = VideoStatus.PENDING
        video.save()
        try:
            enqueue_video_processing(video.id)
        except Exception:
            logger.exception("failed to enqueue video %s", video.id)
            messages.error(request, "Upload saved but processing could not start.")
            return redirect("dashboard")
        messages.success(request, "Video uploaded. Processing has started.")
        return redirect("scanline", video.id)
    return render(request, "dashboard/upload.html", {"form": form})


@login_required(login_url="/accounts/login", redirect_field_name="")
def scanline(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    _require_video_owner(request, video)
    if request.method == "POST":
        scanline_raw = request.POST.get("scanline_slider")
        if scanline_raw is None:
            messages.error(request, "Scanline position is required.")
            return redirect("scanline", video_id)
        try:
            scanline_x = int(scanline_raw)
            service = VideoProcessingService()
            summary_bytes = service.create_scanline_summary(video, scanline_x)
            summary_name = f"{video.uploaded_by}_{video.videofile.name.split('/')[-1]}_smrtsummary.jpg"
            video.video_summary.save(summary_name, ContentFile(summary_bytes))
            return redirect("video_summary", video_id)
        except (ValueError, PermissionError) as exc:
            messages.error(request, str(exc))
        except Exception:
            logger.exception("summary generation failed for video %s", video_id)
            messages.error(request, "Could not generate summary. Try again.")
        return redirect("scanline", video_id)
    return render(request, "dashboard/scanline.html", {"video": video})


@login_required(login_url="/accounts/login", redirect_field_name="")
def video_summary(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    _require_video_owner(request, video)
    if not video.video_summary:
        messages.error(request, "No summary available yet.")
        return redirect("scanline", video_id)
    return render(
        request,
        "dashboard/video_summary.html",
        {
            "video": video,
            "video_summary": video.video_summary,
            "frame_count": video.frame_count,
        },
    )


@require_GET
def health(request):
    return JsonResponse({"status": "ok"})


@login_required(login_url="/accounts/login")
def video_status(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    _require_video_owner(request, video)
    return JsonResponse(
        {
            "id": video.id,
            "status": video.status,
            "processing_error": video.processing_error,
            "frame_count": video.frame_count,
            "frame_width": video.frame_width,
        }
    )
