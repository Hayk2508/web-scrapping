from django.contrib import admin

from parsers.models import (
    VideoParsedObject,
    ImageParsedObject,
    ImageParser,
    VideoParser,
)


@admin.register(ImageParsedObject)
class ImageParsedObjectAdmin(admin.ModelAdmin):
    list_display = ("id", "image_url")
    search_fields = ("image_url",)


@admin.register(VideoParsedObject)
class VideoParsedObjectAdmin(admin.ModelAdmin):
    list_display = ("id", "video_url")
    search_fields = ("video_url",)


@admin.register(VideoParser)
@admin.register(ImageParser)
class ParserAdmin(admin.ModelAdmin):
    list_display = ("id", "url")
    search_fields = ("url",)
