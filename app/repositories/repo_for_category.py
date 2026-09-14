from sqlalchemy import String, cast, or_
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import (
    CreateOrUpdateCategoryRequest,
    UpdateCategoryRequest,
)


def is_category_exists(
    db: Session, name: str | None = None, id: int | None = None
) -> bool:
    # Проверяем существует ли категория с заданным именем
    if name is not None:
        return get_category_by_name(db, name) is not None
    # Проверяем существует ли категория с заданным идентификатором
    elif id is not None:
        return get_category_by_id(db, id) is not None
    # Проверяем существует ли хотя бы одна категория (любое название и любой идентификатор)
    else:
        return db.query(Category.id).first() is not None
        # raise ValueError("It is necessary to provide either a name or a category ID")


def create_category(db: Session, dto: CreateOrUpdateCategoryRequest) -> Category:
    # Создаем новую категорию и добавляем ее в БД
    category = Category(**dto.model_dump())
    db.add(category)
    db.flush()
    db.refresh(category)
    return category


def get_category_by_id(db: Session, id: int) -> Category:
    # Получаем и возвращаем категорию по идентификатору
    return db.query(Category).filter(Category.id == id).first()


def get_category_by_name(db: Session, name: str) -> Category:
    # Получаем и возвращаем категорию по наименованию
    return db.query(Category).filter(Category.name == name).first()


def get_all_categories(db: Session, text: str | None = None) -> list[Category]:
    # Получаем все категории, если условие НЕ задано
    if text is None or len(text) == 0:
        return db.query(Category).all()

    # Получаем категории по условию, если оно задано
    search_value = f"%{text}%"
    results = (
        db.query(Category)
        .filter(
            or_(
                Category.name.ilike(search_value),
                Category.description.ilike(search_value),
                cast(Category.id, String).like(search_value),
                cast(Category.created_at, String).like(search_value),
            )
        )
        .all()
    )
    return results


def get_all_categories_by_fields(
    db: Session,
    name_filter: list[str] | None = None,
    description_filter: list[str] | None = None,
) -> list[Category]:
    master_conditions = []

    if name_filter:
        condition_by_name = [Category.name.ilike(f"%{value}%") for value in name_filter]
        master_conditions.append(or_(*condition_by_name))

    if description_filter:
        condition_by_description = [
            Category.description.ilike(f"%{value}%") for value in description_filter
        ]
        master_conditions.append(or_(*condition_by_description))

    return db.query(Category).filter(*master_conditions).all()  # Протестировать !!!


def update_category(db: Session, category: UpdateCategoryRequest) -> Category:
    # Получаем категорию, которую следует изменить
    updated = db.query(Category).filter(Category.id == category.id).first()
    # Изменяем категорию
    updated.name = category.name
    updated.description = category.description
    return updated


def update_category_by_id(
    db: Session, id: int, category: CreateOrUpdateCategoryRequest
) -> Category:
    # Получаем категорию, которую следует изменить
    updated = db.query(Category).filter(Category.id == id).first()
    # Изменяем категорию
    updated.name = category.name
    updated.description = category.description
    return updated


def delete_category(db: Session, id: int) -> Category:
    category = get_category_by_id(db, id)
    db.delete(category)
    return category
