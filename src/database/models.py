from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    ...


class BaseIdModel(Base):
    """
    Базовая модель с первичным ключом в виде целочисленного ID.
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    