# Сервис сокращения ссылок (Test Assignment)

## Возможности

1. Сокращение ссылок: `POST /shorten`
2. Перенаправление: `GET /{short_id}` (с инкрементом счетчика просмотров)
3. Статистика: `GET /stats/{short_id}`

## Стек

- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- Alembic (Миграции)
- Pydantic
- Docker & Docker Compose

## Как запустить

### 1. Настройка окружения

Создайте файл `.env` в корневой директории. Вы можете просто скопировать пример из `.env_example` для быстрой проверки:

```bash
cp .env_example .env
```

Или создайте его вручную с содержимым:

```env
POSTGRES_DATABASE_USERNAME=postgres
POSTGRES_DATABASE_PASSWORD=postgres
POSTGRES_DATABASE_HOST=db
POSTGRES_DATABASE_PORT=5432
POSTGRES_DATABASE_NAME=link_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=link_db
```

### 2. Запуск через Docker Compose

```bash
docker compose up --build
```

**Особенности запуска:**
- Данные PostgreSQL сохраняются в именованном volume `postgres_data`.
- Миграции применяются автоматически при запуске контейнера (`alembic upgrade head`).
- API будет доступно по адресу: <http://localhost:8000>

## Работа с миграциями (Alembic)

Если вы изменили модели в `models.py`, создайте новую миграцию:

```bash
docker compose exec api alembic revision --autogenerate -m "Описание изменений"
```

Затем примените её:

```bash
docker compose exec api alembic upgrade head
```

## Тесты

### Запуск в Docker (рекомендуется)

Это самый простой способ, так как все зависимости уже внутри:

```bash
docker compose exec api pytest tests/
```

### Запуск локально

Для запуска тестов локально установите зависимости и запустите pytest:

```bash
pip install -r requirements.txt
python -m pytest tests/
```
