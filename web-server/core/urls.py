from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from parsers.views import ParsedObjectViewSet

router = DefaultRouter()
router.register(r"parsed-objects", ParsedObjectViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/parsers/", include("parsers.urls")),
    path("api/", include(router.urls)),
]
