import base64
import hashlib
import json
import os
import time
from datetime import timedelta, datetime
from typing import Annotated
from google.cloud import kms_v1
import jwt
from fastapi import FastAPI, HTTPException, status, Body
from pydantic import BaseModel
import requests
from jwcrypto import jwk
from enum import Enum

app = FastAPI()
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/User/Desktop/WebScrapping/services/FAuth/key.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/var/secrets/google/key.json"
client = kms_v1.KeyManagementServiceClient()

KMS_KEY_NAME = os.getenv("KMS_KEY_NAME")
KMS_KEY_RING_NAME = os.getenv("KMS_KEY_RING_NAME")

PROJECT_ID = os.getenv("PROJECT_ID")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRATION_TIME = timedelta(minutes=60)
REFRESH_TOKEN_EXPIRATION_TIME = timedelta(days=7)


class TOKEN(Enum):
    ACCESS_TOKEN = "access"
    REFRESH_TOKEN = "refresh"


def get_latest_key_version():
    parent = f"projects/{PROJECT_ID}/locations/global/keyRings/{KMS_KEY_RING_NAME}/cryptoKeys/{KMS_KEY_NAME}"
    versions = client.list_crypto_key_versions(parent=parent)
    max_version = max((int(v.name.split("/")[-1]) for v in versions), default=None)
    return str(max_version)


name = client.crypto_key_version_path(
    PROJECT_ID, "global", KMS_KEY_RING_NAME, KMS_KEY_NAME, get_latest_key_version()
)


def get_jwk():
    get_public_key_request = kms_v1.GetPublicKeyRequest(name=name)
    public_key = client.get_public_key(request=get_public_key_request).pem
    jwk_obj = jwk.JWK.from_pem(public_key.encode("utf-8"))
    return jwk_obj.export(as_dict=True)


class Credential(BaseModel):
    username: str
    password: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


def verify_credentials(data: dict):
    response = requests.post(url="http://104.154.80.137/api/check/", json=data)
    return response.status_code == 200


def create_jwt(
    token_type: str, data: dict, expires_delta: timedelta | None = None
) -> str:
    payload = data.copy()
    expire = datetime.now() + expires_delta

    payload.update(
        {
            "iat": round(time.time()),
            "exp": int(expire.timestamp()),
            "token_type": token_type,
        }
    )

    header = {"alg": ALGORITHM, "typ": "JWT", "kid": get_jwk()["kid"]}
    header_b64 = (
        base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    )
    payload_b64 = (
        base64.urlsafe_b64encode(json.dumps(payload, default=str).encode())
        .decode()
        .rstrip("=")
    )

    message = f"{header_b64}.{payload_b64}"

    digest = hashlib.sha256(message.encode()).digest()

    sign_response = client.asymmetric_sign(
        request={"name": name, "digest": {"sha256": digest}}
    )

    signature_b64 = (
        base64.urlsafe_b64encode(sign_response.signature).decode().rstrip("=")
    )

    return f"{message}.{signature_b64}"


@app.post("/auth/api/token/")
def login_for_tokens(credential: Credential):
    if not verify_credentials(credential.dict()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    credential.dict().pop("password")

    access_token = create_jwt(
        data=credential.dict(),
        expires_delta=ACCESS_TOKEN_EXPIRATION_TIME,
        token_type=TOKEN.ACCESS_TOKEN.value,
    )

    refresh_token = create_jwt(
        data=credential.dict(),
        expires_delta=REFRESH_TOKEN_EXPIRATION_TIME,
        token_type=TOKEN.REFRESH_TOKEN.value,
    )

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@app.post("/auth/api/token/refresh/")
def refresh_token(ref_token: Annotated[str, Body(...)]):
    try:
        payload = jwt.decode(
            ref_token, algorithms=[ALGORITHM], options={"verify_signature": False}
        )

        access_token = create_jwt(
            data=payload,
            expires_delta=ACCESS_TOKEN_EXPIRATION_TIME,
            token_type=TOKEN.ACCESS_TOKEN.value,
        )

        new_refresh_token = create_jwt(
            data=payload,
            expires_delta=REFRESH_TOKEN_EXPIRATION_TIME,
            token_type=TOKEN.REFRESH_TOKEN.value,
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


@app.get("/auth/api/public_key")
def get_public_key():

    return {"public_key": get_jwk()}


# For local test
# if __name__ == "__main__":
#     uvicorn.run(app=app, host="0.0.0.0", port=8001)
