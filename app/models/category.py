from datetime import datetime

# from decimal import Decimal
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column  # , relationship

from app.database import Base


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
    )


# class Product(Base):
#     __tablename__ = "product"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(nullable=False)
#     description: Mapped[str]

#     category: Mapped[list[Category]] = relationship(
#         "Category",
#         back_populates="product",
#         uselist=True,
#     )

#     price: Mapped[Decimal]
#     quantity: Mapped[int]

#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True),
#         server_default=func.now(),
#         nullable=False,
#     )
