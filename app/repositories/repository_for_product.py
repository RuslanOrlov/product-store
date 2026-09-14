from sqlalchemy import String, cast, or_
from sqlalchemy.orm import Session

# from app.models.category import Category
# from app.schemas.category import (
#     CreateOrUpdateCategoryRequest,
#     UpdateCategoryRequest,
# )
from app.models.product import Product
from app.schemas.product import (
    CreateOrUpdateProductRequest,
    UpdateProductRequest,
)


def is_product_exists(
    db: Session, name: str | None = None, id: int | None = None
) -> bool:
    # Проверяем существует ли продукт (товар) с заданным именем И с заданным id
    if name is not None and id is not None:
        return (
            db.query(Product).filter(Product.name == name, Product.id == id).first()
            is not None
        )
    # Проверяем существует ли продукт (товар) с заданным именем
    elif name is not None:
        return get_product_by_name(db, name) is not None
    # Проверяем существует ли продукт (товар) с заданным id
    elif id is not None:
        return get_product_by_id(db, id) is not None
    # Проверяем существует ли хотя бы один продукт (товар) (любое название и любой идентификатор)
    else:
        return db.query(Product.id).first() is not None
        # raise ValueError("It is necessary to provide either a name or a product ID")


def is_product_exists_except_id(db: Session, id: int, name: str) -> bool:
    # Проверяем существует ли продукт (товар) с заданным именем И с другим id
    return (
        db.query(Product).filter(Product.id != id, Product.name == name).first()
        is not None
    )


def create_product(db: Session, dto: CreateOrUpdateProductRequest) -> Product:
    # Создаем новый продукт (товар) и добавляем его в БД
    product = Product(**dto.model_dump())
    db.add(product)
    db.flush()
    db.refresh(product)
    return product


def get_product_by_id(db: Session, id: int) -> Product:
    # Получаем и возвращаем продукт (товар) по идентификатору
    return db.query(Product).filter(Product.id == id).first()


def get_product_by_name(db: Session, name: str) -> Product:
    # Получаем и возвращаем продукт (товар) по наименованию
    return db.query(Product).filter(Product.name == name).first()


def get_all_products(db: Session, text: str | None = None) -> list[Product]:
    # Получаем все продукты (товары), если условие НЕ задано
    if text is None or len(text) == 0:
        return db.query(Product).all()

    # Получаем продукты (товары) по условию, если оно задано
    search_value = f"%{text}%"
    results = (
        db.query(Product)
        .filter(
            or_(
                Product.name.ilike(search_value),
                Product.description.ilike(search_value),
                cast(Product.id, String).like(search_value),
                cast(Product.created_at, String).like(search_value),
            )
        )
        .all()
    )
    return results


def get_all_products_by_fields(
    db: Session,
    name_filter: list[str] | None = None,
    description_filter: list[str] | None = None,
) -> list[Product]:
    master_conditions = []

    if name_filter:
        condition_by_name = [Product.name.ilike(f"%{value}%") for value in name_filter]
        master_conditions.append(or_(*condition_by_name))

    if description_filter:
        condition_by_description = [
            Product.description.ilike(f"%{value}%") for value in description_filter
        ]
        master_conditions.append(or_(*condition_by_description))

    return db.query(Product).filter(*master_conditions).all()  # Протестировать !!!


def update_product(db: Session, product: UpdateProductRequest) -> Product:
    # Получаем продукт (товар), который следует изменить
    updated = db.query(Product).filter(Product.id == product.id).first()
    # Изменяем продукт (товар)
    updated.name = product.name
    updated.description = product.description
    updated.price = product.price
    updated.quantity = product.quantity
    updated.category_id = product.category_id
    return updated


def update_product_by_id(
    db: Session, id: int, product: CreateOrUpdateProductRequest
) -> Product:
    # Получаем продукт (товар), который следует изменить
    updated = db.query(Product).filter(Product.id == id).first()
    # Изменяем продукт (товар)
    updated.name = product.name
    updated.description = product.description
    updated.price = product.price
    updated.quantity = product.quantity
    updated.category_id = product.category_id
    return updated


def delete_product(db: Session, id: int) -> Product:
    product = get_product_by_id(db, id)
    db.delete(product)
    return product
