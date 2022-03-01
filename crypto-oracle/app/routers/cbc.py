from fastapi import APIRouter, Depends
from base64 import b64decode

from app.config import get_app_settings, cbc
from app.dependencies import (
    Token,
    RouteCredentials,
    get_token_for_route,
    validate_scope
)

from app.crypto import (
    Plaintext,
    Challenge,
    derive_key,
    cbc_encrypt
)


router = APIRouter(
    prefix=cbc.prefix,
    tags=["CBC"]
)

route_credentials = RouteCredentials(scope=cbc.scope, password=cbc.password)
validate_access = validate_scope(scope=cbc.scope)
settings = get_app_settings()

key = derive_key(settings.key_seed)
challenge = cbc_encrypt(key, cbc.challenge)
iv = b64decode(challenge.iv)
iv = int.from_bytes(iv, byteorder="big")


@router.post('/token', response_model=Token)
def get_token(token: Token = Depends(get_token_for_route(route_credentials))):
    return token

@router.post("/iv", dependencies=[Depends(validate_access)], response_model=Challenge)
def encrypt_plaintext(plaintext: Plaintext):
    global iv # to avoid iv becoming local to this scope
    iv += cbc.iv_increment
    ciphertext = cbc_encrypt(
        key=key,
        plaintext=plaintext.plaintext,
        iv=iv.to_bytes(16, byteorder="big")
    )
    return ciphertext

@router.get("/iv/challenge", response_model=Challenge)
def read_challenge():
      return challenge
