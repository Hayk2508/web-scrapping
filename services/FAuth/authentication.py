import base64
import hashlib
import json
import os
from datetime import timedelta, datetime, timezone
from typing import Annotated
from google.cloud import kms_v1
import jwt
from fastapi import FastAPI, HTTPException, status, Body
from pydantic import BaseModel
import requests

app = FastAPI()

print("Begin")
ACCESS_TOKEN_EXPIRATION_TIME = timedelta(minutes=60)
REFRESH_TOKEN_EXPIRATION_TIME = timedelta(days=7)
ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"
ALGORITHM = os.getenv("ALGORITHM")

KMS_KEY_NAME = os.getenv("KMS_KEY_NAME")
client = kms_v1.KeyManagementServiceClient()
print("vat chi")
name = client.crypto_key_version_path(
    "winter-clone-429310-f7", "global", "kms-key-ring", "kms-key", "3"
)
print("mdaa")
print(name)
get_public_key_request = kms_v1.GetPublicKeyRequest(name=name)

PUBLIC_KEY = client.get_public_key(request=get_public_key_request).pem
print("a")


class Credential(BaseModel):
    username: str
    password: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


def verify_credentials(data: dict):
    response = requests.post(url="http://34.46.255.166/api/check/", json=data)
    return response.status_code == 200


def create_jwt(
    token_type: str, data: dict, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "token_type": token_type})

    header = {"alg": ALGORITHM, "typ": "JWT"}
    header_b64 = (
        base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b"=").decode()
    )
    payload_b64 = (
        base64.urlsafe_b64encode(json.dumps(to_encode).encode()).rstrip(b"=").decode()
    )

    message = f"{header_b64}.{payload_b64}"

    digest = hashlib.sha256(message.encode()).digest()

    sign_response = client.asymmetric_sign(
        request={"name": KMS_KEY_NAME, "digest": {"sha256": digest}}
    )

    signature_b64 = (
        base64.urlsafe_b64encode(sign_response.signature).rstrip(b"=").decode()
    )

    encoded_jwt = f"{message}.{signature_b64}"

    return encoded_jwt


@app.post("/api/token/")
def login_for_tokens(credential: Credential):
    if not verify_credentials(credential.dict()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_jwt(
        data=credential.dict(),
        expires_delta=ACCESS_TOKEN_EXPIRATION_TIME,
        token_type=ACCESS_TOKEN,
    )
    refresh_token = create_jwt(
        data=credential.dict(),
        expires_delta=REFRESH_TOKEN_EXPIRATION_TIME,
        token_type=REFRESH_TOKEN,
    )

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@app.post("/api/token/refresh/")
def refresh_token(ref_token: Annotated[str, Body(...)]):
    try:
        payload = jwt.decode(ref_token, PUBLIC_KEY, algorithms=[ALGORITHM])
        access_token = create_jwt(
            data=payload,
            expires_delta=ACCESS_TOKEN_EXPIRATION_TIME,
            token_type=ACCESS_TOKEN,
        )
        new_refresh_token = create_jwt(
            data=payload,
            expires_delta=REFRESH_TOKEN_EXPIRATION_TIME,
            token_type=REFRESH_TOKEN,
        )
        return TokenInfo(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/api/public_key")
def get_public_key():
    return {"public_key": PUBLIC_KEY}
