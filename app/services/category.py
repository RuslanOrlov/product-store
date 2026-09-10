from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import category as category_repository
from app.schemas.category import CreateCategoryRequest, GetCategory

# from app.repositories import product as product_repository


def create_category(db: Session, dto: CreateCategoryRequest) -> GetCategory:
    # Проверить, есть ли категория с таким наименованием
    if category_repository.is_category_exists(db=db, name=dto.name):
        # Если категория уже есть, выбрасываем исключение
        raise HTTPException(
            status_code=409, detail=f"Category '{dto.name}' already exists."
        )

    # Иначае создать категорию
    category = category_repository.create_category(db, dto)
    db.commit()

    # Вернуть новую категорию
    return category


def get_category_by_id(db: Session, id: int) -> GetCategory:
    # Проверить, отсутствует ли категория с таким идентификатором
    if not category_repository.is_category_exists(db=db, id=id):
        # Если категории нет, выбрасываем исключение
        raise HTTPException(
            status_code=404, detail=f"Category with given id'{id}' does not exist."
        )

    # Иначе вернуть категорию
    return category_repository.get_category_by_id(db, id)


def get_all_categories(db: Session) -> list[GetCategory]:
    # Вернуть все категории
    return category_repository.get_all_categories(db)


def update_category(db: Session, category: GetCategory) -> GetCategory:
    # Проверить, есть ли категория с таким названием
    if category_repository.is_category_exists(db=db, name=category.name):
        # Если категория уже есть, выбрасываем исключение
        raise HTTPException(
            status_code=409,
            detail=f"Category with given name '{category.name}' already exists.",
        )

    # Иначае обновить категорию
    updated = category_repository.update_category(db, category)
    db.commit()

    # Вернуть измененную категорию
    return updated


def delete_category(db: Session, id: int) -> dict[str, str]:
    # Получить категорию по id
    category = get_category_by_id(db, id)
    # Если категория отсутствует, вернуть сообщение об этом
    if category is None:
        raise HTTPException(
            status_code=404,
            detail=f"Category with given id '{id}' not found",
        )

    # Проверить, есть ли в магазине продукты данной категории
    # if product_repository.is_product_exists_by_category(db, category):

    #     # Если такие продукты есть, выбрасываем исключение
    #     raise HTTPException(
    #         status_code=409,
    #         detail=f"There are products with given category f{category.name} in store",
    #     )

    # Иначе удалить категорию и вернуть сообщение об этом
    category_repository.delete_category(db, id)
    db.commit()
    return {"message": f"Category with given id '{id}' successfully deleted"}
