from django.contrib import admin
from django.contrib.auth.models import User

from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "uploaded_by", "status", "upload_date")
    list_filter = ("status",)
    readonly_fields = ("upload_date", "processing_error")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(uploaded_by=request.user)


admin.site.register(Video, VideoAdmin)
