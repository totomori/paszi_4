# MVP: Регистрация пользователя

Минимальный продукт (MVP), состоящий из:

- **Frontend**: React + Vite + TypeScript  
- **Backend**: FastAPI (Python)  
- **Database**: PostgreSQL  
- **ORM**: SQLAlchemy  
- **Миграции**: Alembic  
- **Хэширование паролей**: Argon2id  
- **Контейнеризация**: Docker + Docker Compose  
- **Тесты**: Pytest  

Проект поднимается командой:

```
docker compose up --build
```

---

# Ожидаемая структура проекта (на гите отсутствуют некоторые файлы, к примеру, .env)

```
project/
│   docker-compose.yml
│   README.md
│   .env
│   .env.example
│
├───backend
│   │   Dockerfile
│   │   start.sh
│   │   requirements.txt
│   │   alembic.ini
│   │
│   ├───alembic
│   │   ├───versions
│   │   │       20250101_create_users_table.py
│   │   env.py
│   │   script.py.mako
│   │
│   ├───app
│   │   │   main.py
│   │   │   config.py
│   │   │   database.py
│   │   │   logging_conf.py
│   │   │
│   │   ├───models
│   │   │       user.py
│   │   ├───routes
│   │   │       register.py
│   │   ├───schemas
│   │   │       user.py
│   │   ├───security
│   │   │       hashing.py
│   │   ├───services
│   │   │       user_service.py
│   │   └───tests
│   │           test_register_success.py
│   │           test_register_duplicate.py
│   │           test_register_weak_password.py
│   │
│   └───tests
│           test_register.py
│
└───frontend
    │   Dockerfile
    │   index.html
    │   package.json
    │   tsconfig.json
    │
    └───src
        │   api.ts
        │   App.tsx
        │   main.tsx
        │
        ├───pages
        │       Register.tsx
        └───styles
                register.css
```

---

# Шаги запуска

## 1. Скопировать проект

```
git clone https://github.com/totomori/paszi_4
cd paszi_4
```

## 2. Создать файл `.env`
Используйте `.env.example` для того, чтобы понять, что в него писать:

И обязательно заполни параметры:


POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
DATABASE_URL=postgresql://postgres:postgres@db:5432/app


## 3. Запустить Docker Compose

Команды для докера:

```
docker compose down -v
docker compose up --build
```

После запуска можно будет открывать странички:  
- для backend → http://localhost:8000  
- для frontend → http://localhost:5173  

---

# Запуск тестов

Чтобы проверить работоспособность MVP были созданы тесты на:
- успешную регистрацию
- дублирующий логин (409 Conflict)  
- слабый пароль (422 Validation Error)

Для их корректной отработни надо очистить базу прежде чем тестировать или же тестировать 1 раз. Иначе 1 тест (на успешную регистрацию) будет провален в связи с уже наличием данного по тесту логина в базе данных.

Команда для запуска тестов (надо находится в корневой директории):

```
docker compose exec backend pytest
```

---

# API

## POST `/api/register`

### Примеры запросов

```json
{
  "login": "логин пользоватля",
  "password": "сложный пароль!"
}
```
*можно писать как в терминал, так и на веб-странице в графический интерфейс

### Примеры ответов

#### 200 OK

```json
{"message": "user создан"}
```

#### 409 Conflict

```json
{"detail": "логин уже существует"}
```

#### 422 Validation Error  

(В нем будет любая ошибка валидации)

---

# CURL-примеры

### Успешная регистрация
```
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"login":"user123","password":"StrongPass1!"}'
```

### Конфликт логина
```
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"login":"user123","password":"StrongPass1!"}'
```

### Ошибка слабого пароля
```
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"login":"weak","password":"123"}'
```

---

# Безопасность: что сделано


1. Не хранится сырой пароль

Пароли хранятся только в `password_hash` (строка Argon2id).

2. Используется Argon2id для улучшения безопасности

Конфигурируемые параметры:

- `ARGON2_TIME_COST`
- `ARGON2_MEMORY_COST`
- `ARGON2_PARALLELISM`
- `ARGON2_HASH_LEN`
- `ARGON2_SALT_LEN`

Параметры задаются в `.env`.

3. Для каждого пользователя создается уникальный логин (unique constraint)

В БД для этого используется:

```
op.create_unique_constraint("uq_users_login", "users", ["login"])
```

4. Присутствует уровень определения "хорошего" пароля

- длина логина  > 8
- допустимые символы  
- надёжность пароля (заглавные, маленькие, цифры, спецсимволы)

5. Пароль не логируется и не выводится в консоль

Для безопасности в консоль при регистрации пользователя выводится только логин.

6. Безопасная конфигурация

- SECRET_KEY находится в .env  
- пароль БД вынесен в переменные окружения  
- миграции строго контролируют структуру таблиц  

---

# Ветки Git

Рекомендуемые ветки:

```
main                — финальная рабочая версия
frontend            — код фронтенда
backend             — код бэка + тесты + алембик
infrastructure      — другие файлы
```

---
