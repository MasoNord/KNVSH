# KNVSH
Телеграм бот для отбражения сведений основных и дополнительных образовательных программах, реализуемых
организациями, расположенными на территории Санкт-Петербурга

https://github.com/user-attachments/assets/06bd41c0-dc03-4d17-8f66-a03da9677ba6

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
```
# Bot Configuration
BOT_TOKEN=<Your Bot Token>
ADMIN_IDS=<Your Admins lists>

# Database Configuration
DB_URL=<Your database specific url>
```

6. Получить токен бота через @BotFather и вставить его в `.env`

7. Запустить бота, для этого выполняем команду с корневой папки:
```
python -m bot.main
```
