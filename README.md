# KNVSH
Телеграм бот для отбражения сведений основных и дополнительных образовательных программах, реализуемых
организациями, расположенными на территории Санкт-Петербурга

https://github.com/user-attachments/assets/40ec0d13-84f2-44c7-a607-5c6d6c8d26a2

# Рабочие Данные
Информация о мероприятиях, проводимых научными и образовательными организациями СанктПетербурга

```
https://researchinspb.ru/api/v1/public/event/
```

Информация о вакансиях научных и образовательных организаций Санкт-Петербурга
```
https://researchinspb.ru/api/v1/public/vacancy/
```

# Технологии
- aiogram
- asyncpg
- pydantic_settings
- SQLAlchemy
- pydantic
- alembic
- PostgreSQL

# Особенности
- Асинхронная обработка запросов
- Реализованы разные сценарии для пользователя и админа
- Возможность добавлять новые вакансии/мероприятия
- Интерактивный просмотр вакансий/мероприятий
- Наличие логирование в проекте

# Структура проекта

```
project
│
├── bot/
│   ├── admin/
│   ├── dao/
│   ├── migrations/
│   ├── user/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
├── .env
├── README.md
├── requirements.txt
```

# Установка
1. Колнировать репозиторий по следующуей ссылке:
```
https://github.com/MasoNord/KNVSH.git
```
2. Перейти в директорию проекта knvsh:
```
cd KNVSH
```
3. Создать и активировать виртуальное окружение:
```
python -m venv venv

# Для Linux
source venv/bin/activate

# Для Windows
venv\Scriptcs\activate
```

4. Установить необходимые зависимости через следующую команду:
```
pip install -r requirements.txt
```

5. Создать файл `.env` в корне проекта:

6. Создание миграции и ее применения:

```
alembic revision --autogenerate -m "revision_name"
alembic upgrade head
```

```
# Bot Configuration
BOT_TOKEN=<Your Bot Token>
MAX_JSON_PAGES_EVENTS=2 # Максимальное количество добавляемых JSON старниц с ссылки на мероприятия
MAX_JSON_PAGES_VACANCIES=2 # Максимальное количество добавляемых JSON старниц с ссылки на вакансии
MAX_ENTITIES_IN_GET_KEYBOARDS=5 # Максимальное количество допустимых сущностей при вызове методов get_events и get_vacancies
ADMIN_IDS=<Your Admins lists>

# Database Configuration
DB_URL=<Your database specific url>
```

7. Получить токен бота через @BotFather и вставить его в `.env`

8. Запустить бота, для этого выполняем команду с корневой папки:
```
python -m bot.main
```
