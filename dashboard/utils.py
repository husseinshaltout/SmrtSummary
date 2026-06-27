from django.conf import settings


def signed_media_url(field_file) -> str:
    if not field_file:
        return ""
    if settings.USE_S3 and hasattr(field_file.storage, "bucket"):
        return field_file.storage.url(
            field_file.name,
            expire=settings.AWS_S3_SIGNED_URL_EXPIRY,
        )
    return field_file.url
