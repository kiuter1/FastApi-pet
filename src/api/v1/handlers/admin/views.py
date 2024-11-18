from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.database import get_db, User


router_admin = APIRouter(tags=["admin"])

@router_admin.get('/a')
async def index(request: Request, db: AsyncSession = Depends(get_db)):
    user = User(name="name", email="email", password="password")
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {'message': 'Hello World!'}