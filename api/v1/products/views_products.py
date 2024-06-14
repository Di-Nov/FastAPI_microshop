from fastapi import APIRouter, HTTPException, status, Depends

from . import crud_products
from core.models.db_helper import db_helper
from api.v1.products.schemas_products import ProductSchema, ProductCreate, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import product_by_id

router = APIRouter(
    prefix="/products",
    tags=[
        "Products",
    ],
)


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product: ProductSchema = Depends(product_by_id),
):
    return await product


@router.get("/", response_model=list[ProductSchema])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud_products.get_products(session=session)


@router.post("/create_product", response_model=ProductSchema)
async def get_products(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud_products.create_product(session=session, product_in=product_in)


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_in: ProductUpdate,
    product: ProductSchema = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud_products.update_product(
        session=session, product=product, product_update=product_in
    )
