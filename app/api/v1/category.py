from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependency import get_db
from app.schemas.category import (
    CreateOrUpdateCategoryRequest,
    GetCategory,
    UpdateCategoryRequest,
)
from app.services import category as category_service

router = APIRouter()


@router.get("/all")
def get_all_categories(
    text: str | None = None,
    db: Session = Depends(get_db),  # noqa: B008
) -> list[GetCategory]:
    return category_service.get_all_categories(db, text)


@router.get("/all-by-fields")
def get_all_categories_by_fields(
    name_filter: list[str] | None = Query(None),  # noqa: B008
    description_filter: list[str] | None = Query(None),  # noqa: B008
    db: Session = Depends(get_db),  # noqa: B008
) -> list[GetCategory]:
    return category_service.get_all_categories_by_fields(db, name_filter, description_filter)


@router.post("/create")
def create_category(
    category: CreateOrUpdateCategoryRequest,
    db: Session = Depends(get_db),  # noqa: B008
) -> GetCategory:
    return category_service.create_category(db, category)


@router.put("/update")
def update_category(
    category: UpdateCategoryRequest,
    db: Session = Depends(get_db),  # noqa: B008
) -> GetCategory:
    return category_service.update_category(db, category)


@router.put("/{id}/update")
def update_category_by_id(
    id: int,
    category: CreateOrUpdateCategoryRequest,
    db: Session = Depends(get_db),  # noqa: B008
) -> GetCategory:
    return category_service.update_category_by_id(db, id, category)


@router.get("/{id}/delete")
def delete_category(id: int, db: Session = Depends(get_db)) -> dict[str, str]:  # noqa: B008
    return category_service.delete_category(db, id)


@router.get("/{id}")
def get_category_by_id(id: int, db: Session = Depends(get_db)) -> GetCategory:  # noqa: B008
    return category_service.get_category_by_id(db, id)
