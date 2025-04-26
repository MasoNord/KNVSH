import os
import logging
from typing import List
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: List[int]
    FORMAT_LOG: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_ROTATION: str = "10 MB"
    MAX_JSON_PAGES_EVENTS: int
    MAX_JSON_PAGES_VACANCIES: int
    MAX_ENTITIES_IN_GET_KEYBOARDS: int
    DB_URL: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

settings = Settings()

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
database_url = settings.DB_URL
dp = Dispatcher()
admins = settings.ADMIN_IDS

logging.basicConfig(level=logging.INFO, format=settings.FORMAT_LOG)
