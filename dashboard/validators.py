from django.core.exceptions import ValidationError


def file_size(value):
    fileSize = value.size
    if fileSize > 419430400:
        raise ValidationError("Maximum file size is 50 MB")
