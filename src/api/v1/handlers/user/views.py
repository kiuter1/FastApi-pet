from email.policy import default

from  jwt.exceptions import InvalidTokenError
from pycparser.ply.lex import TOKEN
from sqlalchemy import  select
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.collections import collection
from starlette import status
from starlette.responses import RedirectResponse

from src.api.v1.database import get_db, User
from src.api.v1.auth import utils
from pydantic import BaseModel
router_user = APIRouter(tags=["user"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

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
async def login(request: Request, username: str = Form(), password: str = Form(),  db: AsyncSession = Depends(get_db)):
    try:
        user = select(User).filter_by(name=username)
        user = await db.execute(user)
        user = user.scalars().first()

        if user and utils.validate_password(password, (user.password)):
            jwt_payload = {
                "sub": str(user.id),
                "username": user.name,
            }
            token = utils.encode_jwt(jwt_payload)
            return TokenInfo(access_token=token, token_type="Bearer")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )


async def get_current_token_payload(request: Request):
    try:
        token: str = await oauth2_scheme(request)
        print(token)
        print(type(token))
        payload = utils.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token {e}"
        )
    return payload


async def get_current_auth_user(request: Request) -> User:
    async for db in get_db():
        payload: dict = await get_current_token_payload(request)
        user_id: str = payload['sub']
        if  user := await db.get(User, user_id):
            request.state.user = user
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token"
        )



@router_user.post("/me")
async def me(request: Request, user: User = Depends(get_current_auth_user)):
    return user


@router_user.get('/go_admin')
async def go_admin(request: Request, user: User = Depends(get_current_auth_user)):
    return RedirectResponse('/user/admin/docs', status_code=301, headers=request.headers)