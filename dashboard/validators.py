from django.core.exceptions import ValidationError


def file_size(value):
    fileSize = value.size
    if fileSize > 26214400:
        raise ValidationError("Maximum file size is 25 MB")


def validate_file_extension(value):
    import os

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [".mp4"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension.")
