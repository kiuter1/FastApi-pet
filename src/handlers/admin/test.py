from . import router_admin
from src.database import get_db, User

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, Depends

@router_admin.get('/a')
async def index(request: Request, db: AsyncSession = Depends(get_db)):
    user = User(name="name", email="email", password="password")
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {'message': 'Hello World!'}