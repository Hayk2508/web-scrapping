from django.contrib import admin

from parsers.models import (
    VideoParsedObject,
    ImageParsedObject,
    ImageParser,
    VideoParser,
)


class ImageParsedObjectAdmin(admin.ModelAdmin):
    list_display = ("id", "image_url")
    search_fields = ("image_url",)


class VideoParsedObjectAdmin(admin.ModelAdmin):
    list_display = ("id", "video_url")
    search_fields = ("video_url",)


class ParserAdmin(admin.ModelAdmin):
    list_display = ("id", "url")
    search_fields = ("url",)


admin.site.register(ImageParsedObject, ImageParsedObjectAdmin)
admin.site.register(VideoParsedObject, VideoParsedObjectAdmin)
admin.site.register(ImageParser, ParserAdmin)
admin.site.register(VideoParser, ParserAdmin)
