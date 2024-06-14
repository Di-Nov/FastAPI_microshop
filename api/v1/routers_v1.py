from fastapi import APIRouter

from api.v1.users.views_users import router as users_router
from api.v1.products.views_products import router as products_router

routers_v1 = APIRouter()
routers_v1.include_router(users_router)
routers_v1.include_router(products_router)


@routers_v1.get("/")
def index():
    return {"message": "hello"}
