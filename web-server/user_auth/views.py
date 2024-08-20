from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.decorators import api_view


@api_view(["POST"])
def verify_user_credentials(request):
    username = request.data.get("username")
    password = request.data.get("password")

    return authenticate(username=username, password=password) is not None
