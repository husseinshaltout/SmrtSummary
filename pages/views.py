from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


def index(request):
    return render(request, "pages/index.html")


@ensure_csrf_cookie
def spa_view(request):
    index_path = Path(settings.BASE_DIR) / "SmrtSummary" / "static" / "frontend" / "index.html"
    if index_path.exists():
        return HttpResponse(index_path.read_text(), content_type="text/html")
    return render(request, "pages/index.html")
