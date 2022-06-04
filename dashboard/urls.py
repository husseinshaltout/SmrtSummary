from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('upload', views.upload, name='upload'),
    path('scanline', views.scanline, name='scanline'),
    path('video_summary', views.video_summary, name='video_summary'),
]
