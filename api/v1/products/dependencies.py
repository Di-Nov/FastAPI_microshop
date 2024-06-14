from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException, Path, Depends
from api.v1.products import crud_products
from core.models import db_helper


async def product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    product = await crud_products.get_product(session=session, product_id=product_id)
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="product not found"
    )
