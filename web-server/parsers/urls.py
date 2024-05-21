from django.contrib import admin
from django.urls import path, include
from .views import parse_content, ParsersApiView

urlpatterns = [
    path("parse", parse_content, name="parse_content"),
    path("parse-content", ParsersApiView.as_view())
]

