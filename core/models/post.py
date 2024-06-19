from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String
from typing import TYPE_CHECKING

from core.models.base import Base
from core.models.mixins.user_relation_mixin import UserRelationMixin

if TYPE_CHECKING:
    from core.models import User


class Post(UserRelationMixin, Base):
    __user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(Text, default="", server_default="")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title})"

    def __repr__(self):
        return self.__str__()
