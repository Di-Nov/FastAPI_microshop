from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.user import User


class UserRelationMixin:
    __user_id_unique: bool = False
    __user_back_populates: str | None = None
    __user_nullable: bool = False

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("users.id"),
            unique=cls.__user_id_unique,
            nullable=cls.__user_nullable,
        )

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship("User", back_populates=cls.__user_back_populates)
