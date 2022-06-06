from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('upload', views.upload, name='upload'),
    path('<int:video_id>', views.scanline, name='scanline'),
    path('video_summary/<int:video_id>', views.video_summary,
         name='video_summary'),
]
