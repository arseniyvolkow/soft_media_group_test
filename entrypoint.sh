#!/bin/sh

# Создаем папку, если её нет
mkdir -p alembic/versions

# Проверяем наличие .py файлов в папке миграций
if ! ls alembic/versions/*.py >/dev/null 2>&1; then
  echo "No migrations found. Generating initial migration..."
  alembic revision --autogenerate -m "Initial auto-migration"
fi

echo "Applying migrations..."
alembic upgrade head

echo "Starting application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
