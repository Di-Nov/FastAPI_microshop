from fastapi import APIRouter, Depends, status

from . import crud_products
from core.db_helper import db_helper
from api.v1.products.schemas_products import (
    ProductSchema,
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
)
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import product_by_id
from core.models.product import Product

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
    return product


@router.get("/", response_model=list[ProductSchema])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud_products.get_products(session=session)


@router.post(
    "/create_product", response_model=ProductSchema, status_code=status.HTTP_201_CREATED
)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud_products.create_product(session=session, product_in=product_in)


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_update: ProductUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud_products.update_product(
        session=session, product=product, product_update=product_update
    )


@router.patch("/{product_id}", response_model=ProductSchema)
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud_products.update_product(
        session=session, product=product, product_update=product_update, partial=True
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud_products.delete_product(session=session, product=product)
