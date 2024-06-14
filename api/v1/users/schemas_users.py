from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated


class CreateUser(BaseModel):

    username: Annotated[str, MinLen(3), MaxLen(20)]
    # username: str = Field(max_length=20, min_length=3)
    email: EmailStr
    password: Annotated[str, MinLen(3), MaxLen(20)]
