from datetime import datetime

from pydantic import BaseModel, Field, field_validator


# Модель для создания новой категории продукта в магазине
class CreateOrUpdateCategoryRequest(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=255)

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
class GetCategory(BaseModel):
    id: int | None = None
    name: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=255)
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
class UpdateCategoryRequest(BaseModel):
    id: int | None = None
    name: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=255)

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
