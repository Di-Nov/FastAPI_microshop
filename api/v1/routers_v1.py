from fastapi import APIRouter

from api.v1.users.views_users import router as users_router
from api.v1.products.views_products import router as products_router
from api.v1.demo_auth.demo_jwt_auth import router as jwt_router
from api.v1.demo_auth.views_auth import router as auth_router

routers_v1 = APIRouter()
routers_v1.include_router(users_router)
routers_v1.include_router(products_router)
routers_v1.include_router(auth_router)
routers_v1.include_router(jwt_router)


@routers_v1.get("/")
def index():
    return {"message": "hello"}
