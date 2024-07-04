from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated


class CreateUser(BaseModel):

    username: Annotated[str, MinLen(3), MaxLen(20)]
    # username: str = Field(max_length=20, min_length=3)
    email: EmailStr
    password: Annotated[str, MinLen(3), MaxLen(20)]


class UserSchema(BaseModel):
    # Должны быть указаны строго те типы, что мы передали в схему.
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: str | None = None
    active: bool = True
