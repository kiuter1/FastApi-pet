from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select, or_
from starlette import status
from src.api.v1.handlers.admin.shemas import TourForm
from src.api.v1.database import get_db, Tour, client
from typing import Annotated
router_admin = APIRouter(tags=["admin"])


# @router_admin.post('/added_tour/photo')
# async def added_tour_photo(request: Request, photo: UploadFile):
#     if photo:
#         print(str(photo))
#         content = await photo.read()
#         if photo.content_type not in ['image/jpeg', 'image/png']:
#             raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
#         url = await client.fput_object()
#
#     return {'message': url}



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
    await db.refresh(tour)
    return {'message': 'Tour registered successfully!'}

