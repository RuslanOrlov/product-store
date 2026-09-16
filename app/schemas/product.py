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
    # category_id: int
    category: GetCategory
    created_at: datetime

    # Валидатор для проверки корректности поля name
    @field_validator("name")
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
    def name_must_be_not_empty(cls, v: str) -> str:
        # Убираем пробелы по краям
        v = v.strip()
        # Проверяем, что строка не пустая
        if not v:
            raise ValueError("Category name cannot be empty")
        # Возвращаем очищенное значение
        return v


# Модель для передачи параметра фильтрации по полю price
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

    # Валидатор для проверки корректности диапазонов значений price
    @field_validator("ranges")
    def validate_couples_of_price(
        cls, value: list[tuple[Decimal, Decimal]]
    ) -> list[tuple[Decimal, Decimal]]:
        for i, (start, end) in enumerate(value, start=1):
            if start > end:
                raise ValueError(
                    f"In couple #{i} start price '{start}' more than end price '{end}'"
                )
        return value


# Модель для передачи параметра фильтрации по полю quantity
class QuantityFilter(BaseModel):
    ranges: list[tuple[int, int]] = Field(
        default_factory=list,
        title="Диапазоны количества товара",
        description=(
            "Список диапазонов количества товара. "
            "Каждый диапазон задаётся как "
            "[минимальное количество, максимальное количество]."
        ),
        examples=[
            [[1, 50], [80, 180]],
        ],
    )

    # Валидатор для проверки корректности диапазонов значений quantity
    @field_validator("ranges")
    def validate_couples_of_quantity(
        cls, value: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        for i, (start, end) in enumerate(value, start=1):
            if start > end:
                raise ValueError(
                    f"In couple #{i} start quantity '{start}' more than end quantity '{end}'"
                )
        return value


# Модель для передачи параметра фильтрации по полю created_at
class CreatedAtFilter(BaseModel):
    ranges: list[tuple[datetime, datetime]] = Field(
        default_factory=list,
        title="Диапазоны дат создания товара",
        description=(
            "Список диапазонов дат создания товара. "
            "Каждый диапазон задаётся как "
            "[начальная дата, конечная дата]."
        ),
        examples=[
            [
                ["2026-09-01T00:00:00", "2026-09-15T23:59:59"],
                ["2026-08-01T00:00:00", "2026-08-31T23:59:59"],
            ],
        ],
    )

    # Валидатор для проверки корректности диапазонов значений created_at
    @field_validator("ranges")
    def validate_couples_of_created_at(
        cls, value: list[tuple[datetime, datetime]]
    ) -> list[tuple[datetime, datetime]]:
        for i, (start, end) in enumerate(value, start=1):
            if start is None or end is None:
                raise ValueError(f"In couple #{i} dates cannot be null")
            if start > end:
                raise ValueError(
                    f"In couple #{i} start date '{start}' more than end date '{end}'"
                )
        return value


# Модель для передачи параметра фильтрации по полю category_id
class ByCategoryFilter(BaseModel):
    ids: list[int] = Field(
        default_factory=list,
        title="Список id категорий продуктов (товаров)",
        description=(
            "Список id категорий продуктов (товаров). "
            "Список задаётся как [id_1, id_2, ..., id_n]."
        ),
        examples=[[1, 2, 4, 8, 11]],
    )

    # Валидатор для проверки корректности значений id категорий продуктов
    @field_validator("ids")
    def validate_filter_field(cls, value: list[int]) -> list[int]:
        if None in value:
            raise ValueError(
                "List contains None values, which are not allowed for filtering."
            )
        for i, v in enumerate(value, start=1):
            if v <= 0:
                raise ValueError(
                    f"Value #{i} is zero or negative: '{v}'. All values must be positive."
                )
        return value
