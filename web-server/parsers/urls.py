from django.contrib import admin
from django.urls import path, include
from .views import parse_content, ppppp, ddddd

urlpatterns = [
    path("parse/", parse_content, name="parse_content"),
    path("pp", ppppp, name="pp"),
    path("dd", ddddd, name="dd"),
]
