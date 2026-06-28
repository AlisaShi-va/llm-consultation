# Двухсервисная система LLM-консультаций
________________________________________
### Архитектура
```
auth_service/
├── .env
├── pyproject.toml
└── app/
    ├── main.py
    ├── core/
    │   ├── config.py
    │   ├── security.py
    │   └── exceptions.py
    ├── db/
    │   ├── base.py
    │   ├── session.py
    │   └── models.py
    ├── schemas/
    │   ├── auth.py
    │   └── user.py
    ├── repositories/
    │   └── users.py
    ├── usecases/
    │   └── auth.py
    └── api/
        ├── deps.py
        ├── router.py
        └── routes_auth.py

bot_service/
├── .env
├── pyproject.toml
├── pytest.ini
└── app/
    ├── main.py
    ├── core/
    │   ├── config.py
    │   └── jwt.py
    ├── infra/
    │   ├── redis.py
    │   └── celery_app.py
    ├── tasks/
    │   └── llm_tasks.py
    ├── services/
    │   └── openrouter_client.py
    ├── bot/
    │   ├── dispatcher.py
    │   └── handlers.py
    └── tests/
        └── conftest.py
```

### Описание
- Auth Service (FastAPI) - предоставляет веб-API. В сервисе реализованы регистрация пользователя, вход (логин) и выдача JWT. Сервис хранит пользователей в базе данных SQLite, хранит пароль в виде хеша и формирует JWT с полями sub (id пользователя), role и временем жизни;
* Endpoint-ы:* 
-- POST /auth/register создаёт пользователя
-- POST /auth/login возвращает JWT
-- GET /auth/me возвращает профиль по JWT
- Bot Service - содержит Telegram-бота на aiogram и реализует логику: бот принимает сообщения пользователя, проверяет наличие JWT и валидирует его. Если токен валиден, бот отправляет запрос к LLM и возвращает ответ. Если токен отсутствует или неверный, бот отказывает в доступе и просит пользователя авторизоваться через Auth Service

### Пользовательский сценарий
1. Регистрация пользователя и получение токена в Auth Service
2. Команда /token <jwt> для передачи токена боту
3. Сохранение токена с привязкой к user_id
4. Запрос к LLM с валидным токеном

#### Результаты
- Проверка работы эндпоинтов (Из Postman, т.к. у меня нет впн, чтобы работать с OpenAPI)
<img width="908" height="680" alt="запрос1" src="https://github.com/user-attachments/assets/44f87cb9-a7f9-4fa2-b2b5-739b0d4ac974" />

<img width="917" height="599" alt="запрос1+" src="https://github.com/user-attachments/assets/0de383e1-edc9-4644-8d5f-3a5d10210deb" />

<img width="1023" height="574" alt="запрос2" src="https://github.com/user-attachments/assets/76401f74-40bd-4a63-8641-19cae5ddd822" />

<img width="1102" height="640" alt="запрос2+" src="https://github.com/user-attachments/assets/4c3a6403-0e5b-4b00-b5a5-9861e87ec7d4" />

<img width="605" height="363" alt="запрос3" src="https://github.com/user-attachments/assets/9abadd72-13bb-4f6e-98d4-f4f702dbc36b" />

- Проверка работы RabbitMQ
<img width="1840" height="944" alt="2026-06-28_02-33-08" src="https://github.com/user-attachments/assets/6d10f474-a5e6-4091-957c-8d307140be2b" />

- Проверка работы бота (так и не удалась, я уже задолбалась с этими прокси, повторюсь, что нет впн, с телефона с прокси бот тоже не захотел общаться)
<img width="1080" height="2108" alt="Screenshot_20260628_133144_Telegram" src="https://github.com/user-attachments/assets/aba67fa2-84e4-4953-aa33-5c3fafd0f690" />

