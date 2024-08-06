from django.contrib import admin

from parsers.models import (
    VideoParsedObject,
    ImageParsedObject,
    ImageParser,
    VideoParser,
)


class BaseAdmin(admin.ModelAdmin):
    list_display = ("id", "url")
    search_fields = ("url",)


admin.site.register(ImageParsedObject, BaseAdmin)
admin.site.register(VideoParsedObject, BaseAdmin)
admin.site.register(ImageParser, BaseAdmin)
admin.site.register(VideoParser, BaseAdmin)
