from src.api.v1.core.settings import app
from src.api.v1.handlers.admin import app_admin, router_admin
from src.api.v1.handlers.user import app_user, router_user

app_admin.include_router(router_admin)
app_user.include_router(router_user)

app_user.mount("/admin", app_admin)
app.mount("/user", app_user,)