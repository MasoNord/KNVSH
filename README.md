# KNVSH
Телеграм бот для отопражения сведений основных и дополнительных образовательных программах, реализуемых
организациями, расположенными на территории Санкт-Петербурга

# Рабодчие Данные
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

# Наполнение .env файла
```
# Bot Configuration
BOT_TOKEN=<Your Bot Token>

# Database Configuration
ADMIN_IDS=<Your Admins lists>
DB_URL=<Your database specific url>
```