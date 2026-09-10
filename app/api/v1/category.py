from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependency import get_db
from app.schemas.category import CreateCategoryRequest, GetCategory
from app.services import category as category_service

router = APIRouter()


@router.post("/create")
def create_category(
    category: CreateCategoryRequest, db: Session = Depends(get_db)
) -> GetCategory:
    return category_service.create_category(db, category)


@router.get("/{id}")
def get_category_by_id(id: int, db: Session = Depends(get_db)) -> GetCategory:
    return category_service.get_category_by_id(db, id)


@router.get("/all")
def get_all_categories(db: Session = Depends(get_db)) -> list[GetCategory]:
    return category_service.get_all_categories(db)


@router.put("/update")
def update_category(
    category: GetCategory, db: Session = Depends(get_db)
) -> GetCategory:
    return category_service.update_category(db, category)


@router.get("/{id}/delete")
def delete_category(id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    return category_service.delete_category(db, id)
