from sqlalchemy import  select
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.v1.database import get_db, User
from src.api.v1.auth import utils
from pydantic import BaseModel
router_user = APIRouter(tags=["user"])


class TokenInfo(BaseModel):
    access_token: str
    token_type: str

@router_user.post('/regesregistration')
async def index(request: Request, name:str, password: str, email: str, db: AsyncSession = Depends(get_db)):
    user = User(name=name, email=email, password=utils.hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {'message': 'User registered successfully!'}


@router_user.post("/login", response_model=TokenInfo)
async def login(request: Request, name: str, password: str,  db: AsyncSession = Depends(get_db)):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    if (user := await db.get(User, name)) and utils.validate_password(password, user.password):
        jwt_payload = {
            "sub": user.id,
            "username": user.name,
        }

        token = utils.encode_jwt(jwt_payload)
        return TokenInfo(access_token=token, token_type="Bearer")
    else:
        raise unauthed_exc
