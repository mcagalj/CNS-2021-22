from pydantic import BaseModel
from fastapi import APIRouter, Depends

from app.config import arp
from app.dependencies import (
    Token,
    RouteCredentials,
    get_token_for_route,
    validate_scope
)

from app.crypto import (
    Challenge, 
    derive_key,
    encrypt_challenge
)

router = APIRouter(
    prefix=arp.prefix,
    tags=["ARP"]
)

route_credentials = RouteCredentials(scope=arp.scope, password=arp.password)
validate_access = validate_scope(scope=arp.scope)

class Cookie(BaseModel):
    cookie: str
    
cookie = Cookie(cookie=arp.cookie)
key = derive_key(arp.cookie)
challenge = encrypt_challenge(key, arp.challenge)

@router.post('/token', response_model=Token)
def get_token(token: Token = Depends(get_token_for_route(route_credentials))):
    return token
    
@router.get("/cookie", dependencies=[Depends(validate_access)], response_model=Cookie)
def read_challenge():
      return cookie

@router.get("/challenge", response_model=Challenge)
def read_challenge():
      return challenge