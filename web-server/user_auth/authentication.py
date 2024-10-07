import json
from cryptography.hazmat.primitives import serialization
from django.contrib.auth import get_user_model
from rest_framework import authentication, status
import jwt
from django.core.cache import cache
import requests
from rest_framework_simplejwt.exceptions import AuthenticationFailed


def get_public_key_from_auth():
    response = requests.get(url="http://104.154.80.137/auth/api/public_key/")

    if response.status_code == 200:
        return response.json()["public_key"]


def to_cache(public_key, kid: str):
    cache.set("public_key", public_key)
    cache.set("kid", kid)


def convert_to_pem(public_key):
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(public_key))
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return public_key_pem.decode("utf-8")


class MyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationFailed(code=status.HTTP_401_UNAUTHORIZED)

        token = request.META["HTTP_AUTHORIZATION"].split("Bearer ")[1]
        public_key = cache.get("public_key")
        kid = jwt.get_unverified_header(token)["kid"]

        if not public_key or kid != cache.get("kid"):
            public_key = get_public_key_from_auth()
            to_cache(public_key=public_key, kid=kid)

        public_key_pem = convert_to_pem(public_key)
        decoded_token = jwt.decode(token, public_key_pem, algorithms=["RS256"])

        return get_user_model().objects.get(username=decoded_token["username"]), None
