from django.contrib import admin
from .models import VideoParsedObject, ImageParser, VideoParser, ImageParsedObject

# Register your models here.


admin.site.register(VideoParsedObject)
admin.site.register(ImageParsedObject)
admin.site.register(ImageParser)
admin.site.register(VideoParser)
