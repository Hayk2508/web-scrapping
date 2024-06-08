from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from parsers.views import ImageParsedObjectViewSet, VideoParsedObjectViewSet

router = DefaultRouter()
router.register(r"image-parsed-objects", ImageParsedObjectViewSet)
router.register(r"video-parsed-objects", VideoParsedObjectViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/parsers/", include("parsers.urls")),
    path("api/", include(router.urls)),
]
