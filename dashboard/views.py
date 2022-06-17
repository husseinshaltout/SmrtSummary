from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseNotFound
from .forms import VideoForm
from .models import Video
from .smrtsummary import SmrtSummary
from django.conf import settings
import os
from django.contrib.auth.decorators import login_required
from django.core.files import File


def isExist(path) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


@login_required(login_url="/accounts/login", redirect_field_name="")
def home(request):
    videos = Video.objects.order_by("-upload_date").filter(uploaded_by=request.user)
    context = {
        "uploaded_videos": videos,
    }
    return render(request, "dashboard/video_listings.html", context)


@login_required(login_url="/accounts/login", redirect_field_name="")
def upload(request, user_id=None):
    form = VideoForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.uploaded_by = request.user
            obj.save()
            path = f"{settings.MEDIA_ROOT}/frames/{str(obj.uploaded_by.id)}/{os.path.basename(obj.videofile.name)}"
            isExist(path)
            summary = SmrtSummary(str(obj.videofile.path), path)
            obj.video_duration = summary.get_video_duration()[0]
            obj.save()
            summary.split_to_frames()
            # create thumbnail and add it to db
            # thumnailFrame = summary.get_video_duration()[1] // 2
            thumnailFrame = "1"
            thumbData = open(os.path.join(path, f"frame{thumnailFrame}.jpg"), "rb")
            thumbFile = File(thumbData)
            obj.thumbnail.save("thumbnail.jpg", thumbFile)
            form = VideoForm()
            return redirect("scanline", obj.id)
    return render(request, "dashboard/upload.html", {"form": form})


@login_required(login_url="/accounts/login", redirect_field_name="")
def scanline(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if video.uploaded_by != request.user:
        return HttpResponseNotFound("<h1>Not authenticated</h1>")
    else:
        if request.method == "POST":
            scanlineValue = request.POST["scanline_slider"]

            summary = SmrtSummary(
                str(video.videofile.path),
                f"{settings.MEDIA_ROOT}/frames/{str(video.uploaded_by.id)}/{os.path.basename(video.videofile.name)}",
            )

            path = f"{settings.MEDIA_ROOT}/frames/{str(video.uploaded_by.id)}/{os.path.basename(video.videofile.name)}/cropped"
            isExist(path)
            summary.create_summary(int(scanlineValue))
            # create video_summary and add it to db
            smrtsummaryData = open(os.path.join(path, "summary.png"), "rb")
            smrtsummaryFile = File(smrtsummaryData)
            video.video_summary.save("smrtsummary.jpg", smrtsummaryFile)
            return redirect("video_summary", video_id)
        else:
            context = {"video": video}
            return render(request, "dashboard/scanline.html", context)


@login_required(login_url="/accounts/login", redirect_field_name="")
def video_summary(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if video.uploaded_by != request.user:
        return HttpResponseNotFound("<h1>Not authenticated</h1>")
    else:
        context = {"video_summary": video.video_summary}
    return render(request, "dashboard/video_summary.html", context)
