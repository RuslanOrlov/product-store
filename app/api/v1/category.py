from fastapi import APIRouter

from app.schemas.category import CreateCategoryRequest, GetCategory
from app.services import category as category_service

router = APIRouter()


@router.post("/create")
def create_category(category: CreateCategoryRequest):
    return category_service.create_category(category)


@router.get("/{id}")
def get_category_by_id(id: int):
    return category_service.get_category_by_id(id)


@router.get("/all")
def get_all_categories():
    return category_service.get_all_categories()


@router.put("/update")
def update_category(category: GetCategory):
    return category_service.update_category(category)


@router.get("/{id}/delete")
def delete_category(id: int):
    return category_service.delete_category(id)
