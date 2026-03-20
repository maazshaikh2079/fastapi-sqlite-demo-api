from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, Integer

# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass


# SQLAlchemy ORM / DB Model
class Order(Base):
    """SQLAlchemy model for the 'orders' table."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    item_name: Mapped[str] = mapped_column(String, index=True, nullable=False)

    quantity: Mapped[int] = mapped_column(Integer, default=0)

    price: Mapped[float] = mapped_column(Float,  nullable=False)
