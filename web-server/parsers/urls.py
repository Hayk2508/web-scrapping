from django.contrib import admin
from django.urls import path, include

from parsers.views import parse_content

urlpatterns = [
    path("parse", parse_content, name="parse_content")
]

