from typing import List
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📊 Статистика", callback_data = "statistic")
    kb.button(text="🎟️ Добавить мероприятия", callback_data = "add_events")
    kb.button(text="💼 Добавить вакансии", callback_data = "add_vacancies")
    kb.button(text="🏠 На главную", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()


def main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⚙️ Админ панель", callback_data="admin_panel")
    kb.button(text="📆 Посмотреть мероприятния", callback_data="get_events")
    kb.button(text="📢 Посмотреть вакансии", callback_data="get_vacancies")
    kb.adjust(1)
    return kb.as_markup()

def add_events_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📑 Добавить мероприятия через JSON файл", callback_data = "add_events_by_file")
    kb.button(text="🌐 Добавить мероприятия по ссылке на JSON файл", callback_data = "add_events_by_url")
    kb.button(text="🏠 На главную", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()

def add_vacancy_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📑 Добавить вакансию через JSON файл", callback_data = "add_vacancies_by_file")
    kb.button(text="🌐 Добавить вакансию по ссылке на JSON файл", callback_data = "add_vacancies_by_url")
    kb.button(text="🏠 На главную", callback_data="home")
    kb.adjust(1)
    return kb.as_markup()

def cancel_kb_inline() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Отмена", callback_data="cancel")
    return kb.as_markup()

def continue_add_new_events() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Добавить еще", callback_data="add_events")
    kb.button(text="⚙️ Админ панель", callback_data="admin_panel")
    kb.adjust(2)
    return kb.as_markup()