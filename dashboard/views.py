from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseNotFound
from .forms import VideoForm
from .models import Video
from .smrtsummary import SmrtSummary
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile


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
            summary = SmrtSummary(str(obj.videofile.url))
            obj.video_duration = summary.get_video_duration()[0]
            obj.save()
            splittedFramesList = summary.split_to_frames()
            framesAsNpz = summary.store_frames_npz(splittedFramesList)
            video_framesContentFile = ContentFile(
                framesAsNpz, name=f"{str(obj.uploaded_by)}_{str(obj.videofile.name).split('/')[-1]}.npz"
            )
            obj.video_frames = video_framesContentFile
            print("Saving npz file")
            obj.save()
            # create thumbnail and add it to db
            # thumbnailFrame = summary.get_video_duration()[1] // 2
            thumbnailFrame = 1
            thumbData = summary.create_thumbnail(splittedFramesList, thumbnailFrame)
            thumbnailContentFile = ContentFile(thumbData, name="thumbnail.jpg")
            obj.thumbnail.save("thumbnail.jpg", thumbnailContentFile)
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
            summary = SmrtSummary(str(video.videofile.url))
            # create video_summary and add it to db
            smrtsummaryData = summary.create_summary(int(scanlineValue), f"media/{str(video.video_frames.name)}")
            smrtsummaryFile = ContentFile(
                smrtsummaryData,
                name=f"{str(video.uploaded_by.id)}/{str(video.videofile.name).split('/')[-1]}_smrtsummary.jpg",
            )
            video.video_summary.save(
                f"{str(video.uploaded_by)}_{str(video.videofile.name).split('/')[-1]}_smrtsummary.jpg", smrtsummaryFile
            )
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
