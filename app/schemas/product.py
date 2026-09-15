from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.schemas.category import GetCategory


# Модель для создания нового продукта в магазине
class CreateOrUpdateProductRequest(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=255)
    price: Decimal = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    category_id: int = Field(..., gt=0)

    # Валидатор для проверки корректности поля name
    @field_validator("name")
    # @classmethod
    def name_must_be_not_empty(cls, v: str) -> str:
        # Убираем пробелы по краям
        v = v.strip()
        # Проверяем, что строка не пустая
        if not v:
            raise ValueError("Category name cannot be empty")
        # Возвращаем очищенное значение
        return v


# Модель для возврата категории продукта из <- БД
class GetProduct(BaseModel):
    id: int | None = None
    name: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=255)
    price: Decimal = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    category: GetCategory
    created_at: datetime

    # Валидатор для проверки корректности поля name
    @field_validator("name")
    # @classmethod
    def name_must_be_not_empty(cls, v: str) -> str:
        # Убираем пробелы по краям
        v = v.strip()
        # Проверяем, что строка не пустая
        if not v:
            raise ValueError("Category name cannot be empty")
        # Возвращаем очищенное значение
        return v


# Модель для изменения категории продукта в -> БД
class UpdateProductRequest(BaseModel):
    id: int | None = None
    name: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=255)
    price: Decimal = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    category_id: int = Field(..., gt=0)

    # Валидатор для проверки корректности поля name
    @field_validator("name")
    # @classmethod
    def name_must_be_not_empty(cls, v: str) -> str:
        # Убираем пробелы по краям
        v = v.strip()
        # Проверяем, что строка не пустая
        if not v:
            raise ValueError("Category name cannot be empty")
        # Возвращаем очищенное значение
        return v


# Модель для передачи параметра фильтрации price
class PriceFilter(BaseModel):
    ranges: list[tuple[Decimal, Decimal]] = Field(
        default_factory=list,
        title="Диапазоны цен",
        description=(
            "Список диапазонов цен. "
            "Каждый диапазон задаётся как "
            "[минимальная цена, максимальная цена]."
        ),
        examples=[
            [[20, 50], [99.99, 151.50]],
        ],
    )

    @field_validator("ranges")
    # @classmethod
    def validate_couples_of_price(
        cls, value: list[tuple[Decimal, Decimal]]
    ) -> list[tuple[Decimal, Decimal]]:
        for i, (start, end) in enumerate(value, start=1):
            if start > end:
                raise ValueError(
                    f"In couple #{i} start price '{start}' more than end price '{end}'"
                )
        return value
