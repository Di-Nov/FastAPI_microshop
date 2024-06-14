from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated


class ProductBase(BaseModel):
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductUpdatePartial(ProductBase):
    name: str | None = None
    description: str | None = None
    price: int | None = None


class ProductSchema(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductDelete(BaseModel):
    pass
