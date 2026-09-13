from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import repository_for_category as category_repository

# from app.schemas.category import (
#     CreateOrUpdateCategoryRequest,
#     GetCategory,
#     UpdateCategoryRequest,
# )
from app.repositories import repository_for_product as product_repository
from app.schemas.product import (
    CreateOrUpdateProductRequest,
    GetProduct,
    UpdateProductRequest,
)


def get_all_products(db: Session, text: str | None = None) -> list[GetProduct]:
    # Вернуть все продукты (товары)
    return product_repository.get_all_products(db, text)


def get_all_products_by_fields(
    db: Session,
    name_filter: list[str] | None = None,
    description_filter: list[str] | None = None,
) -> list[GetProduct]:
    # Вернуть все продукты (товары) в соответствии с фильтром
    return product_repository.get_all_products_by_fields(
        db, name_filter, description_filter
    )


def create_product(db: Session, dto: CreateOrUpdateProductRequest) -> GetProduct:
    # Проверить, есть ли хотя бы одна категория в БД
    if not category_repository.is_category_exists(db):
        # Если нет ни одной категории, выбрасываем исключение
        raise HTTPException(
            status_code=404,
            detail="There is no category in database. Create at least one category before create products.",
        )

    # Проверить, есть ли категория с необходимым id в БД
    if not category_repository.is_category_exists(db=db, id=dto.category_id):
        # Если категории с необходимым id нет, выбрасываем исключение
        raise HTTPException(
            status_code=404,
            detail=f"There is no category with given id '{dto.category_id}' in database.",
        )

    # Проверить, есть ли продукт (товар) с таким наименованием
    if product_repository.is_product_exists(db=db, name=dto.name):
        # Если продукт (товар) уже есть, выбрасываем исключение
        raise HTTPException(
            status_code=409, detail=f"Product '{dto.name}' already exists."
        )

    # Иначе создать продукт (товар)
    product = product_repository.create_product(db, dto)
    db.commit()

    # Вернуть новый продукт (товар)
    return product


def update_product(db: Session, product: UpdateProductRequest) -> GetProduct:
    # Проверить, есть ли продукт (товар) с таким id
    if not product_repository.is_product_exists(db=db, id=product.id):
        # Если продукт (товар) отсутствует, выбрасываем исключение
        raise HTTPException(
            status_code=404,
            detail=f"Product with expected id '{product.id}' does not exist.",
        )
    # Проверить, есть ли продукт (товар) с таким названием
    # if product_repository.is_product_exists(db=db, name=product.name):
    #     # Если продукт (товар) с таким названием уже есть, выбрасываем исключение
    #     raise HTTPException(
    #         status_code=409,
    #         detail=f"Product with given name '{product.name}' already exists.",
    #     )

    # Проверить, есть ли категория с необходимым id в БД
    if not category_repository.is_category_exists(db=db, id=product.category_id):
        # Если категории с необходимым id нет, выбрасываем исключение
        raise HTTPException(
            status_code=404,
            detail=f"There is no category with given id '{product.category_id}' in database.",
        )

    # Иначе обновить продукт (товар)
    updated = product_repository.update_product(db, product)
    db.commit()

    # Вернуть измененный продукт (товар)
    return updated


def update_product_by_id(
    db: Session, id: int, product: CreateOrUpdateProductRequest
) -> GetProduct:
    # Проверить, есть ли продукт (товар) с таким id
    if not product_repository.is_product_exists(db=db, id=id):
        # Если продукт (товар) отсутствует, выбрасываем исключение
        raise HTTPException(
            status_code=404,
            detail=f"Product with given id '{id}' does not exist.",
        )
    # Проверить, есть ли продукт (товар) с таким названием
    # if product_repository.is_product_exists(db=db, name=product.name):
    #     # Если продукт (товар) с таким названием уже есть, выбрасываем исключение
    #     raise HTTPException(
    #         status_code=409,
    #         detail=f"Product with given name '{product.name}' already exists.",
    #     )

    # Проверить, есть ли категория с необходимым id в БД
    if not category_repository.is_category_exists(db=db, id=product.category_id):
        # Если категории с необходимым id нет, выбрасываем исключение
        raise HTTPException(
            status_code=404,
            detail=f"There is no category with given id '{product.category_id}' in database.",
        )

    # Иначе обновить продукт (товар)
    updated = product_repository.update_product_by_id(db, id, product)
    db.commit()

    # Вернуть измененный продукт (товар)
    return updated


def delete_product(db: Session, id: int) -> dict[str, str]:
    # Получить продукт (товар) по id
    product = get_product_by_id(db, id)
    # Если продукт (товар) отсутствует, вернуть сообщение об этом
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with given id '{id}' not found",
        )

    # Иначе удалить продукт (товар) и вернуть сообщение об этом
    product_repository.delete_product(db, id)
    db.commit()
    return {"message": f"Product with given id '{id}' successfully deleted"}


def get_product_by_id(db: Session, id: int) -> GetProduct:
    # Проверить, отсутствует ли продукт (товар) с таким id
    if not product_repository.is_product_exists(db=db, id=id):
        # Если продукта нет, выбрасываем исключение
        raise HTTPException(
            status_code=404, detail=f"Product with given id'{id}' does not exist."
        )

    # Иначе вернуть продукт (товар)
    return product_repository.get_product_by_id(db, id)
