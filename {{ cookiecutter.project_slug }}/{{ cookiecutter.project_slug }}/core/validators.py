from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings

def kilobytes(n):
    return n * 1024;

def megabytes(n):
    return kilobytes(n) * 1024

def image_size_validator(image):
    if image.size > (megabytes(settings.MAX_IMAGE_UPLOAD_SIZE_MB)):
        message = _('The file exceed the maximum size of %(max_size)s MB.')
        params = {'max_size': settings.MAX_IMAGE_UPLOAD_SIZE_MB}
        raise ValidationError(message, params=params)
