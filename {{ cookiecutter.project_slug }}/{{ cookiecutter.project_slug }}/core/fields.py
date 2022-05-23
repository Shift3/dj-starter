from rest_framework import serializers
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from django.conf import settings


class ThumbnailField(serializers.ImageField):
    def _get_url(self, url):
        if url is not None and url.startswith("http"):
            return url

        return (f"{settings.SERVER_URL}{url}",)

    def to_representation(self, instance):
        if not instance:
            return None

        res = {
            "file": {
                "url": self._get_url(instance.url),
            },
            "thumbnails": [],
        }
        for key, value in settings.THUMBNAIL_ALIASES[""].items():
            res["thumbnails"].append(
                {
                    "size": key,
                    "file": {
                        "url": self._get_url(thumbnail_url(instance, key)),
                    },
                }
            )
        return res
