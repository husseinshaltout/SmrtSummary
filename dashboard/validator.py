from django.core.exceptions import ValidationError


def file_size(value):
    fileSize = value.size
    if fileSize > 1000:
        raise ValidationError("Maximum file size is 1 GB")
