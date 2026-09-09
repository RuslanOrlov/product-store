from app.schemas.category import CreateCategoryRequest, GetCategory


def is_category_exists(name: str | None = None, id: int | None = None) -> bool:
    """
    Проверяет, существует ли категория с заданным именем или идентификатором.
    :param name: Имя категории для проверки.
    :param id: Идентификатор категории для проверки.
    :return: True, если категория существует, иначе False.
    """
    if name is not None:
        pass  # Логика проверки существования категории по имени
    elif id is not None:
        pass  # Логика проверки существования категории по идентификатору
    else:
        raise ValueError("It is necessary to provide either a name or a category ID")


def create_category(category: CreateCategoryRequest):
    pass  # Логика создания категории


def get_category_by_id(id: int):
    pass  # Логика получения категории по идентификатору


def get_all_categories():
    pass  # Логика получения всех категорий


def update_category(category: GetCategory):
    pass  # Логика обновления категории


def delete_category(id: int):
    pass  # Логика удаления категории
