from fastapi import FastAPI, Depends

from src.api.v1.handlers.user.views import get_current_auth_user
from src.api.v1.middlewares import AdminMiddleware

app_admin = FastAPI(dependencies=[Depends(get_current_auth_user)])
app_admin.add_middleware(AdminMiddleware)