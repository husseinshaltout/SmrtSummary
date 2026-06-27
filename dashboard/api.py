from typing import Optional

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Router, Schema
from ninja.security import django_auth

from dashboard.forms import VideoForm
from dashboard.models import Video, VideoStatus
from dashboard.services import VideoProcessingService
from dashboard.tasks import enqueue_video_processing
from dashboard.utils import signed_media_url

api = NinjaAPI(csrf=True, urls_namespace="api")
auth_router = Router(tags=["auth"])
videos_router = Router(tags=["videos"], auth=django_auth)


class RegisterSchema(Schema):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str
    password2: str


class LoginSchema(Schema):
    username: str
    password: str


class UserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str


class VideoSchema(Schema):
    id: int
    title: str
    status: str
    video_duration: str
    frame_count: int
    frame_width: int
    upload_date: str
    thumbnail_url: Optional[str] = None
    summary_url: Optional[str] = None
    video_url: Optional[str] = None
    processing_error: str = ""


class SummaryRequestSchema(Schema):
    scanline: int


def _video_payload(video: Video) -> dict:
    return {
        "id": video.id,
        "title": video.title,
        "status": video.status,
        "video_duration": video.video_duration,
        "frame_count": video.frame_count,
        "frame_width": video.frame_width,
        "upload_date": video.upload_date.isoformat(),
        "thumbnail_url": signed_media_url(video.thumbnail) if video.thumbnail else None,
        "summary_url": signed_media_url(video.video_summary) if video.video_summary else None,
        "video_url": signed_media_url(video.videofile) if video.videofile else None,
        "processing_error": video.processing_error,
    }


def _require_owner(request: HttpRequest, video: Video) -> None:
    if video.uploaded_by_id != request.user.id:
        raise PermissionDenied("You do not have access to this video.")


@auth_router.post("/register", response={201: UserSchema, 400: dict})
def register(request, payload: RegisterSchema):
    if payload.password != payload.password2:
        return 400, {"detail": "Passwords do not match"}
    if User.objects.filter(username=payload.username).exists():
        return 400, {"detail": "Username is taken"}
    if User.objects.filter(email=payload.email).exists():
        return 400, {"detail": "Email is in use"}
    user = User.objects.create_user(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        first_name=payload.firstname,
        last_name=payload.lastname,
    )
    auth_login(request, user)
    return 201, UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )


@auth_router.post("/login", response={200: UserSchema, 401: dict})
def login_view(request, payload: LoginSchema):
    user = authenticate(request, username=payload.username, password=payload.password)
    if user is None:
        return 401, {"detail": "Invalid credentials"}
    auth_login(request, user)
    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )


@auth_router.post("/logout")
def logout_view(request):
    auth_logout(request)
    return {"detail": "logged out"}


@auth_router.get("/me", response=UserSchema, auth=django_auth)
def me(request):
    user = request.user
    return UserSchema(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
    )


@videos_router.get("", response=list[VideoSchema])
def list_videos(request):
    videos = Video.objects.filter(uploaded_by=request.user)
    return [_video_payload(video) for video in videos]


@videos_router.post("", response={201: VideoSchema, 400: dict})
def upload_video(request):
    form = VideoForm(request.POST, request.FILES)
    if not form.is_valid():
        return 400, {"detail": form.errors.as_json()}
    video = form.save(commit=False)
    video.uploaded_by = request.user
    video.status = VideoStatus.PENDING
    video.save()
    enqueue_video_processing(video.id)
    return 201, _video_payload(video)


@videos_router.get("/{video_id}", response=VideoSchema)
def get_video(request, video_id: int):
    video = get_object_or_404(Video, pk=video_id)
    _require_owner(request, video)
    return _video_payload(video)


@videos_router.get("/{video_id}/status")
def video_status_api(request, video_id: int):
    video = get_object_or_404(Video, pk=video_id)
    _require_owner(request, video)
    return _video_payload(video)


@videos_router.post("/{video_id}/summary", response={200: VideoSchema, 400: dict})
def create_summary(request, video_id: int, payload: SummaryRequestSchema):
    video = get_object_or_404(Video, pk=video_id)
    _require_owner(request, video)
    try:
        summary_bytes = VideoProcessingService().create_scanline_summary(video, payload.scanline)
        summary_name = f"{video.uploaded_by}_{video.videofile.name.split('/')[-1]}_smrtsummary.jpg"
        video.video_summary.save(summary_name, ContentFile(summary_bytes))
    except ValueError as exc:
        return 400, {"detail": str(exc)}
    return _video_payload(video)


api.add_router("/auth", auth_router)
api.add_router("/videos", videos_router)
