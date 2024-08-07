from django.urls import path
from .views import parse_content

urlpatterns = [path("parse/", parse_content, name="parse_content")]
