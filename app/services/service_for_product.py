from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import repo_for_category as category_repository

# from app.schemas.category import (
#     CreateOrUpdateCategoryRequest,
#     GetCategory,
#     UpdateCategoryRequest,
# )
from app.repositories import repo_for_product as product_repository
from app.schemas.product import (
    CreateOrUpdateProductRequest,
    GetProduct,
    UpdateProductRequest,
)


def get_all_products(db: Session, text: str | None = None) -> list[GetProduct]:
    # Вернуть все продукты (товары), ЕСЛИ фильтр text НЕ ЗАДАН. Иначе вернуть
    # только продукты (товары), которые соответствуют фильтру text, ЕСЛИ он ЗАДАН
    return product_repository.get_all_products(db, text)


def get_all_products_by_fields(
    db: Session,
    name_filter: list[str] | None = None,
    description_filter: list[str] | None = None,
) -> list[GetProduct]:
    # Вернуть все продукты (товары) в соответствии с фильтром по полям, ЕСЛИ они ЗАДАНЫ
    # В противном случае вернуть все продукты (товары), ЕСЛИ значения фильтра НЕ ЗАДАНЫ
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
    # Проверить, есть ли продукт (товар) с таким же названием, но с другим id
    if product_repository.is_product_exists_except_id(
        db=db, id=product.id, name=product.name
    ):
        # Если продукт (товар) с таким названием уже принадлежит другому id, выбрасываем исключение
        raise HTTPException(
            status_code=409,
            detail=f"Product with given name '{product.name}' already exists with different id.",
        )

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
    # Проверить, есть ли продукт (товар) с таким же названием, но с другим id
    if product_repository.is_product_exists_except_id(db=db, id=id, name=product.name):
        # Если продукт (товар) с таким названием уже принадлежит другому id, выбрасываем исключение
        raise HTTPException(
            status_code=409,
            detail=f"Product with given name '{product.name}' already exists with different id.",
        )

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
        # Если продукта (товара) нет, выбрасываем исключение
        raise HTTPException(
            status_code=404,
            detail=f"Product with given id'{id}' does not exist.",
        )

    # Иначе вернуть продукт (товар)
    return product_repository.get_product_by_id(db, id)


def change_price(db: Session, id: int, price: Decimal) -> GetProduct:
    # Проверить, есть ли продукт (товар) с таким id
    if not product_repository.is_product_exists(db=db, id=id):
        # Если продукта (товара) нет, выбрасываем исключение
        raise HTTPException(
            status_code=404,
            detail=f"Product with given id '{id}' does not exist.",
        )

    # Иначе сохранить изменения цены в БД
    updated = product_repository.change_price(db=db, id=id, price=price)
    db.commit()

    # Вернуть измененный продукт (товар)
    return updated


def add_quantity(db: Session, id: int, quantity: int) -> GetProduct:
    # Проверить, есть ли продукт (товар) с указанным id
    if not product_repository.is_product_exists(db=db, id=id):
        # Если продукта (товара) нет, выбрасываем исключение
        raise HTTPException(
            status_code=404, detail=f"Product with given id '{id}' does not exist."
        )

    # Иначе добавить количество продукта (товара)
    updated = product_repository.add_quantity(db=db, id=id, quantity=quantity)
    db.commit()

    # Вернуть измененный продукт (товар)
    return updated


def subtract_quantity(db: Session, id: int, quantity: int) -> GetProduct:
    # Проверить, есть ли продукт (товар) с указанным id
    if not product_repository.is_product_exists(db=db, id=id):
        # Если продукта (товара) нет, выбрасываем исключение
        raise HTTPException(
            status_code=404,
            detail=f"Product with given id '{id}' does not exist.",
        )

    # Проверить, достаточно ли количество продукта (товара), чтобы уменьшить его
    current = product_repository.get_product_by_id(db=db, id=id).quantity
    if current < quantity:
        # Если количество продукта (товара) недостаточное, выбрасываем исключение
        raise HTTPException(
            status_code=409,
            detail=f"Quantity of current product '{current}' is insufficient to subtract '{quantity}' from it.",
        )

    # Иначе уменьшить количество продукта (товара)
    updated = product_repository.subtract_quantity(db=db, id=id, quantity=quantity)
    db.commit()

    # Вернуть измененный продукт (товар)
    return updated
