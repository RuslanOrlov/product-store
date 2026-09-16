FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Установка системных пакетов, если нужны для PostgreSQL/psycopg/sqlalchemy
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание виртуального окружения в контейнере
RUN python -m venv $VIRTUAL_ENV

# Копируем только requirements.txt, чтобы кэшировать слой зависимостей
COPY requirements.txt .

# Установка зависимостей в venv
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

EXPOSE 8000

# Запуск приложения в режиме разработки
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]