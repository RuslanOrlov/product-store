from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database import SessionLocal


# Получение сессии подключения к БД
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Пример получения сессии через внедрение зависимости:
# def some_function(db: Session = Depends(get_db)):
