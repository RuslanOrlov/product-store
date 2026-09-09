from fastapi import HTTPException

from app.schemas.category import CreateCategoryRequest, GetCategory
from app.repositories import category as category_repository
from app.repositories import product as product_repository


def create_category(category: CreateCategoryRequest):
    # Проверить, есть ли категория с таким наименованием
    if category_repository.is_category_exists(category.name):

        # Если категория уже есть, выбрасываем исключение
        raise HTTPException(
            status_code=409, detail=f"Category '{category.name}' already exists."
        )

    # Иначае создать категорию
    new_category = category_repository.create_category(category)

    # Вернуть новую категорию
    return new_category


def get_category_by_id(id: int):
    # Проверить, отсутствует ли категория с таким идентификатором
    if not category_repository.is_category_exists(id):

        # Если категории нет, выбрасываем исключение
        raise HTTPException(
            status_code=404, detail=f"Category with given id'{id}' does not exist."
        )

    # Иначе вернуть категорию
    return category_repository.get_category_by_id(id)


def get_all_categories():
    # Вернуть все категории
    return category_repository.get_all_categories()


def update_category(category: GetCategory):
    # Проверить, есть ли категория с таким названием
    if category_repository.is_category_exists(category.name):

        # Если категория уже есть, выбрасываем исключение
        raise HTTPException(
            status_code=409,
            detail=f"Category with given name '{category.name}' already exists.",
        )

    # Иначае обновить категорию
    updated = category_repository.update_category(category)
    # Вернуть измененную категорию
    return updated


def delete_category(id: int):
    # Получить категорию по id
    category = get_category_by_id(id)

    # Проверить, есть ли в магазине продукты данной категории
    if product_repository.is_product_exists_by_category(category):

        # Если такие продукты есть, выбрасываем исключение
        raise HTTPException(
            status_code=409,
            detail=f"There are products with given category f{category.name} in store",
        )

    # Иначе удалить категорию
    category_repository.delete_category(id)
    return {"message": f"Category with given id '{id}' successfully deleted"}
