from django.contrib import admin
from django.urls import path, include
from .views import parse_content, return_8, throw_error

urlpatterns = [
    path("parse/", parse_content, name="parse_content"),
    path("r8", return_8, name="r8"),
    path("err", throw_error, name="err"),
]
