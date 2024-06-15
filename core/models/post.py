from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text
from typing import TYPE_CHECKING

from core.models import Base

if TYPE_CHECKING:
    from core.models import User


class Post(Base):
    title: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column(Text, default="", server_default="")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
    )
    user: Mapped["User"] = relationship(back_populates="posts")
