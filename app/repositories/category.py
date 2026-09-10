from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CreateCategoryRequest, GetCategory


def is_category_exists(
    db: Session, name: str | None = None, id: int | None = None
) -> bool:
    # Проверяем существует ли категория с заданным именем
    if name is not None:
        return get_category_by_name(db, name) is not None
    # Проверяем существует ли категория с заданным идентификатором
    elif id is not None:
        return get_category_by_id(db, id) is not None
    else:
        raise ValueError("It is necessary to provide either a name or a category ID")


def create_category(db: Session, dto: CreateCategoryRequest) -> Category:
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


def get_all_categories(db: Session) -> list[Category]:
    # Получаем все категории
    return db.query(Category).all()


def update_category(db: Session, category: GetCategory) -> Category:
    # Получаем категорию, которую следует изменить
    updated = db.query(Category).filter(Category.id == category.id).first()
    # Изменяем категорию
    updated.name = category.name
    updated.description = category.description
    return updated


def delete_category(db: Session, id: int) -> Category:
    category = get_category_by_id(db, id)
    db.delete(category)
    return category
