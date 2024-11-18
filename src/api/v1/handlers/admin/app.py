from fastapi import FastAPI
from src.api.v1.middlewares import AdminMiddleware

app_admin = FastAPI()
app_admin.add_middleware(AdminMiddleware)