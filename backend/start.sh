#!/bin/sh
set -e

# Ждём пока Postgres будет готов
echo "Ожидание запуска базы данных..."
until pg_isready -h db -U $POSTGRES_USER; do
  sleep 1
done

# Пробуем миграции
echo "Запуск Alembic миграций..."
alembic upgrade head || echo "Alembic миграции завершились с ошибкой, продолжаем запуск."

# Запуск приложения
echo "Запуск FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
