from django.contrib import admin
from django.urls import include, path, re_path

from dashboard.api import api
from dashboard.views import health
from pages.views import spa_view

urlpatterns = [
    path("", include("pages.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
    path("api/", api.urls),
    path("health/", health, name="health"),
    path("admin/", admin.site.urls),
    re_path(r"^app(?:/.*)?$", spa_view, name="spa"),
]
