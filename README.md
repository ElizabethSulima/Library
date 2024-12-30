# FastAPI Web Application

## Обзор

Этот проект представляет собой веб-приложение, построенное с использованием FastAPI для урпавления библиотечным каталогом.
API позволяет работать с книгами, авторами и выдачей книг читателям.

## Установка

Для настройки приложения выполните команды:

1. Клонируйте репозиторий
2. Установите зависимости: bash pip install -r requirements.txt
3. poetry install
4. pre-commit install
5. pre-commit run --all-files

## Запуск БД

COMPOSE_FILE=""
DB_HOST=""
DB_COLLECTION=""
PYTHONPATH=""

## Команды для docker compose

docker compose up --build -d
docker compose down -v
docker compose exec имя*контейнера psql -U имя*пользователя имя_бд

## Запуск тестов

pytest
