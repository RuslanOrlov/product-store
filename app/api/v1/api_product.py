from decimal import Decimal

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session

from app.dependency import get_db
from app.schemas.product import (
    ByCategoryFilter,
    CreatedAtFilter,
    CreateOrUpdateProductRequest,
    GetProduct,
    PriceFilter,
    QuantityFilter,
    UpdateProductRequest,
)
from app.services import service_for_product as product_service

router = APIRouter()


@router.get("/all")
def get_all_products(
    text: str | None = None,
    category_name: str | None = None,
    db: Session = Depends(get_db),  # noqa: B008
) -> list[GetProduct]:
    return product_service.get_all_products(db, text, category_name)


@router.post("/all-by-fields")
def get_all_products_by_fields(
    name_filter: list[str] | None = Body(None),  # noqa: B008
    description_filter: list[str] | None = Body(None),  # noqa: B008
    price_filter: PriceFilter | None = Body(None),  # noqa: B008
    quantity_filter: QuantityFilter | None = Body(None),  # noqa: B008
    created_at_filter: CreatedAtFilter | None = Body(None),  # noqa: B008
    category_filter: ByCategoryFilter | None = Body(None),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
) -> list[GetProduct]:
    return product_service.get_all_products_by_fields(
        db,
        name_filter,
        description_filter,
        price_filter,
        quantity_filter,
        created_at_filter,
        category_filter,
    )


@router.post("/create")
def create_product(
    product: CreateOrUpdateProductRequest,
    db: Session = Depends(get_db),  # noqa: B008
) -> GetProduct:
    return product_service.create_product(db, product)


@router.put("/update")
def update_product(
    product: UpdateProductRequest,
    db: Session = Depends(get_db),  # noqa: B008
) -> GetProduct:
    return product_service.update_product(db, product)


@router.put("/{id}/update")
def update_product_by_id(
    id: int,
    product: CreateOrUpdateProductRequest,
    db: Session = Depends(get_db),  # noqa: B008
) -> GetProduct:
    return product_service.update_product_by_id(db, id, product)


@router.get("/{id}/delete")
def delete_product(id: int, db: Session = Depends(get_db)) -> dict[str, str]:  # noqa: B008
    return product_service.delete_product(db, id)


@router.get("/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)) -> GetProduct:  # noqa: B008
    return product_service.get_product_by_id(db, id)


@router.get("/{id}/change-price")
def change_price(
    id: int,
    price: Decimal = Query(..., gt=0),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
) -> GetProduct:
    return product_service.change_price(db=db, id=id, price=price)


@router.get("/{id}/add-quantity")
def add_quantity(
    id: int,
    quantity: int = Query(..., gt=0),
    db: Session = Depends(get_db),  # noqa: B008
) -> GetProduct:
    return product_service.add_quantity(db=db, id=id, quantity=quantity)


@router.get("/{id}/subtract-quantity")
def subtract_quantity(
    id: int,
    quantity: int = Query(..., gt=0),
    db: Session = Depends(get_db),  # noqa: B008
) -> GetProduct:
    return product_service.subtract_quantity(db=db, id=id, quantity=quantity)
