from django.shortcuts import render


def home(request):
    return render(request, 'dashboard/video_listings.html')


def upload(request):
    return render(request, 'dashboard/upload.html')


def scanline(request):
    return render(request, 'dashboard/scanline.html')


def video_summary(request):
    return render(request, 'dashboard/video_summary.html')
