# QRKot
Проект QRKot — это фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Используемые технологии:
* Python
* FastAPI
* Sqlalchemy
* Alembic
* Uvicorn

## Как запустить проект:

1. Клонировать репозиторий и перейти в него в командной строке:

    ```
    git clone git@github.com:AndreyLeshchev/cat_charity_fund_FastApi.git
    ```
    ```
    cd cat_charity_fund_FastApi
    ```

2. Cоздать и активировать виртуальное окружение:
    
    ```
    python3 -m venv env
    ```
    
    * Если у вас Linux/macOS
    
        ```
        source env/bin/activate
        ```
    
    * Если у вас windows
    
        ```
        source venv/Scripts/activate
        ```
    
3. Обновить pip и установить зависимости из файла requirements.txt:

    ```
    python -m pip install --upgrade pip
    ```
    ```
    pip install -r requirements.txt
    ```
    
4. Выполнить миграции:

    ```
    alembic upgrade head
    ```

    Запустить проект:
    ```
    uvicorn app.main:app
    ```

## Примеры API запросов и ответов:

* Для получения JWT токена:

   
    > POST http://127.0.0.1:8000/auth/jwt/login

    Пример запроса:

    ```
    {
        "username": "string",
        "password": "string"
    }
    ```

    Пример ответа:

    ```
    {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2ZDMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ.M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
        "token_type": "bearer"
    }
    ```


* Для создания проекта:

    > POST http://127.0.0.1:8000/charity_project/


    Пример запроса:

    ```
    {
        "name": "string",
        "description": "string",
        "full_amount": 0
    }
    ```

    Пример ответа:

    ```
    {
        "name": "string",
        "description": "string",
        "full_amount": 0,
        "id": 0,
        "invested_amount": 0,
        "fully_invested": true,
        "create_date": "2019-08-24T14:15:22Z",
        "close_date": "2019-08-24T14:15:22Z"
    }
    ```

* Для получения списка donation:

    > GET http://127.0.0.1:8000/donation/


    Пример ответа:

    ```
    [
        {
            "full_amount": 0,
            "comment": "string",
            "id": 0,
            "create_date": "2019-08-24T14:15:22Z",
            "user_id": 0,
            "invested_amount": 0,
            "fully_invested": true,
            "close_date": "2019-08-24T14:15:22Z"
        }
    ]
    ```

### Автор - [Андрей Лещев](https://github.com/AndreyLeshchev)