from django.contrib import admin

from parsers.models import VideoParsedObject, ImageParsedObject

admin.site.register(ImageParsedObject)
admin.site.register(VideoParsedObject)
