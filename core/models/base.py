from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True  #  Таблица не создается

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls):
        """Создает автоматически имена таблиц в дочерних классов"""
        return f"{cls.__name__.lower()}s"
