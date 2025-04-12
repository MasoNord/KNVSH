from typing import List
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📊 Статистика", callback_data = "statistic")
    kb.button(text="🎟️ Добавить мероприятия", callback_data ="add_events")
    kb.button(text="💼 Добавить вакансии", callback_data = "add_vacancies")
    return kb.as_markup()


def main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⚙️Админ панель", callback_data="admin_panel")
    kb.button(text="📆Посмотреть мероприятния", callback_data="get_events")
    kb.button(text="📢Посмотреть вакансии", callback_data="get_vacancies")
    return kb.as_markup()