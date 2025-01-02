from datetime import timedelta

from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select, or_
from starlette import status

from src.api.v1.handlers.admin.shemas import TourForm, DelTourForm
from src.api.v1.database import get_db, Tour, client, Photo
import io

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