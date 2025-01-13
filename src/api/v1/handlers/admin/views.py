import io
from datetime import timedelta

from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File
from sqlalchemy import select, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from src.api.v1.database import get_db, Tour, client, Photo, User, Order
from src.api.v1.handlers.admin.shemas import TourForm, DelTourForm, UserChangeForm, OrderChangeForm, DelOrderForm

router_admin = APIRouter(tags=["admin"])


@router_admin.post('/added_tour/photo')
async def added_tour_photo(request: Request, files: UploadFile = File(...)):
    content = await files.read()
    await client.put_object("photo", files.filename, io.BytesIO(content), length=-1, part_size=10*1024*1024,)
    url = await client.get_presigned_url("GET","photo", files.filename, timedelta(days=7))
    return {'photo_url': url}



@router_admin.post('/added_tour')
async def added_tour(request: Request, tour_form:TourForm, db: AsyncSession = Depends(get_db)):
    tour = select(Tour).where(or_(Tour.name == tour_form.name, Tour.location == tour_form.location))
    tour = await db.execute(tour)
    tour = tour.scalars().first()
    if tour:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Tour already exists!",
        )
    tour = Tour(name=tour_form.name, location=tour_form.location, description=tour_form.description, price=tour_form.price)
    db.add(tour)
    await db.commit()
    if tour_form.photo:
        tour_db = select(Tour).filter_by(name=tour_form.name)
        tour_db = await db.execute(tour_db)
        tour_db = tour_db.scalars().first()
        for i in tour_form.photo:
            photo_name = i.get("name")
            photo_url = i.get("response").get("photo_url")
            photo = Photo(url=photo_url, filename=photo_name, tour_id=tour_db.id)
            db.add(photo)
        await db.commit()
    return {'message': 'Tour registered successfully!'}


@router_admin.post('/deleted_tour')
async def deleted_tour(request: Request, deleted_tour:DelTourForm, db: AsyncSession = Depends(get_db)):
    tour = await db.get(Tour, deleted_tour.id)
    if tour is None:
        return {"error": "Tour not found"}
    await db.delete(tour)
    await db.commit()
    return {'status': 'ok'}



@router_admin.post('/edit_tour')
async def edit_tour(request: Request, tour_form: TourForm, db: AsyncSession = Depends(get_db)):
    # Проверяем существование тура по ID
    tour = await db.get(Tour, tour_form.id)
    if tour is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tour not found!",
        )

    tour.name = tour_form.name or tour.name
    tour.location = tour_form.location or tour.location
    tour.description = tour_form.description or tour.description
    tour.price = tour_form.price or tour.price

    if tour_form.photo:
        old_photos = await db.execute(select(Photo).where(Photo.tour_id == tour.id))
        old_photos = old_photos.scalars().all()
        for photo in old_photos:
            await db.delete(photo)

        for i in tour_form.photo:
            photo_name = i.get("name")
            photo_url = i.get("response").get("photo_url")
            photo = Photo(url=photo_url, filename=photo_name, tour_id=tour.id)
            db.add(photo)


    await db.commit()

    return {'status': 'ok', 'message': 'Tour updated successfully!'}


@router_admin.get('/users')
async def users(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User.id, User.name, User.email, User.is_admin))
    user_list = result.all()
    return [{"id": user[0], "name": user[1], "email": user[2], "is_admin": user[3],}for user in user_list]

@router_admin.post('/change_user')
async def change_user(request: Request, user_change_form: UserChangeForm, db: AsyncSession = Depends(get_db)):
    try:
        user = await db.get(User, user_change_form.id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_admin = user_change_form.is_admin
        db.add(user)
        await db.commit()

        return {"message": "User updated successfully"}

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")


@router_admin.get('/orders')
async def get_tours(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        query = select(Order).options(joinedload(Order.tour), joinedload(Order.user).load_only(User.id, User.name, User.email))  # Загрузка связанного объекта Tour
        result = await db.execute(query)
        orders = result.scalars().all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return orders


@router_admin.post('/change_order')
async def change_user(request: Request, order_change_form: OrderChangeForm, db: AsyncSession = Depends(get_db)):
    try:
        order = await db.get(Order, order_change_form.id)
        if not order:
            raise HTTPException(status_code=404, detail="User not found")
        order.is_done = order_change_form.is_done
        db.add(order)
        await db.commit()

        return {"message": "User updated successfully"}

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")


@router_admin.post('/deleted_order')
async def deleted_tour(request: Request, deleted_order:DelOrderForm, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, deleted_order.id)
    if order is None:
        return {"error": "Order not found"}
    await db.delete(order)
    await db.commit()
    return {'status': 'ok'}