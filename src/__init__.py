from .database import init_db
from .core import app



@app.on_event('startup')
async def startup():
    await init_db()