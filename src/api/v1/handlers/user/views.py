import datetime


from  jwt.exceptions import InvalidTokenError
from sqlalchemy import  select, or_
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from src.api.v1.handlers.user.shemas import TokenInfo, RegistrationForm, LoginForm, OrderForm
from src.api.v1.database import get_db, User, Photo, Tour, client, Order
from src.api.v1.auth import utils
router_user = APIRouter(tags=["user"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


@router_user.post('/registration')
async def register(request: Request, user_form:RegistrationForm, db: AsyncSession = Depends(get_db)):
    user = select(User).where(or_(User.name == user_form.username, User.email == user_form.email))
    user = await db.execute(user)
    user = user.scalars().first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already taken",
        )
    user = User(name=user_form.username, email=user_form.email, password=utils.hash_password(user_form.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {'message': 'User registered successfully!'}


@router_user.post("/login", response_model=TokenInfo)
async def login(request: Request, user_form: LoginForm,  db: AsyncSession = Depends(get_db)):
    try:
        user_db = select(User).filter_by(name=user_form.username)
        user_db = await db.execute(user_db)
        user_db = user_db.scalars().first()

        if user_db and utils.validate_password(user_form.password, (user_db.password)):
            jwt_payload = {
                "sub": str(user_db.id),
                "username": user_db.name,
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



@router_user.get("/me")
async def me(request: Request, user: User = Depends(get_current_auth_user)):
    return user


@router_user.get('/tours')
async def get_tours(request: Request, db: AsyncSession = Depends(get_db)):
    datatime_request = int(datetime.datetime.now().timestamp())
    try:
        query = select(Tour).options(joinedload(Tour.photo))
        result = await db.execute(query)
        tours = result.unique().scalars().all()

        response = []
        for tour in tours:
            updated_photos = []
            if tour.photo:
                for photo in tour.photo:
                    if datatime_request - photo.url_updated >= 7 * 24 * 60 * 60:
                        new_url = await client.get_presigned_url(
                            "GET", "photo", photo.filename, datetime.timedelta(days=7)
                        )
                        photo.url = new_url
                        photo.url_updated = datatime_request
                        db.add(photo)

                    updated_photos.append({
                        "id": photo.id,
                        "url": photo.url,
                    })

            response.append({
                "id": tour.id,
                "name": tour.name,
                "location": tour.location,
                "description": tour.description,
                "price": tour.price,
                "photos": updated_photos,
            })

        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return response


@router_user.post('/create_order')
async def create_order(request: Request, order_form: OrderForm, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_auth_user)):
    order = Order(fullname=order_form.fullName, contact=order_form.contact, persons=order_form.people, comments=order_form.comments,tour_id=order_form.tour_id, user_id=user.id)
    db.add(order)
    await db.commit()
    return {'status': 'ok'}
