from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.models.base import Base
from core.models.mixins.user_relation_mixin import UserRelationMixin


class Profile(Base, UserRelationMixin):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))
    bio: Mapped[str | None]
