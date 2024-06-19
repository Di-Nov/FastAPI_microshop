from typing import TYPE_CHECKING

from sqlalchemy import String


from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.user_relation_mixin import UserRelationMixin

if TYPE_CHECKING:
    from core.models import Post
    from core.models import Profile


class User(Base):
    username: Mapped[str] = mapped_column(String(30), unique=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username})"

    def __repr__(self):
        return self.__str__()
