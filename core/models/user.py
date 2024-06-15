from sqlalchemy import String


from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Product(Base):
    username: Mapped[str] = mapped_column(String(30), unique=True)
