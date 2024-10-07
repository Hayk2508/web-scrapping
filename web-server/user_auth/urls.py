from django.urls import path

from user_auth.views import verify_user_credentials

urlpatterns = [
    path("check/", verify_user_credentials, name="verify_user_credentials"),
]
