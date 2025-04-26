from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging

from bot.config import settings

def main_user_kb(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="📆Посмотреть мероприятния", callback_data="get_events")
    kb.button(text="📢Посмотреть вакансии", callback_data="get_vacancies")
    if user_id in settings.ADMIN_IDS:
        kb.button(text="⚙️ Админ панель", callback_data="admin_panel")
    kb.adjust(1)
    return kb.as_markup()

def get_events_kb(events, start) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    adjust_elements = []
    for i in range(len(events[start])):
        adjust_elements.append(1)
        kb.button(text=f"{events[start][i]}", callback_data=f"get_event_by_{i}")

    adjust_elements.append(3)

    if start == 0:
        kb.button(text="❌", callback_data="back_to_list_denied")
    else:
        kb.button(text="⬅️", callback_data="back_to_list_events")

    kb.button(text=f"{start + 1}/{len(events)}", callback_data="reminder")
    
    if start == len(events) - 1:
        kb.button(text="❌", callback_data="forward_to_list_denied")
    else:
        kb.button(text="➡️", callback_data="forward_to_list_events")
    
    adjust_elements.append(1)
    kb.button(text="🏠 На главную", callback_data="home")

    kb.adjust(*adjust_elements,3)
    return kb.as_markup()

def get_vacancies_kb(vacancies, start) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    adjust_elements = []
    for i in range(len(vacancies[start])):
        adjust_elements.append(1)
        kb.button(text=f"{vacancies[start][i]}", callback_data=f"get_vacancy_by_{i}")
    
    adjust_elements.append(3)
    if start == 0:
        kb.button(text="❌", callback_data="back_to_list_denied")
    else:
        kb.button(text="⬅️", callback_data="back_to_list_vacancies")

    kb.button(text=f"{start + 1}/{len(vacancies)}", callback_data="reminder")
    
    if start == len(vacancies) - 1:
        kb.button(text="❌", callback_data="forward_to_list_denied")
    else:
        kb.button(text="➡️", callback_data="forward_to_list_vacancies")
    
    adjust_elements.append(1)
    kb.button(text="🏠 На главную", callback_data="home")

    kb.adjust(*adjust_elements,3)
    return kb.as_markup()

def back_to_event_list() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Вернуться к спсику мероприятий", callback_data="get_events")
    kb.adjust(1)
    return kb.as_markup()

def back_to_vacancys_list() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Вернуться к спсику вакансий", callback_data="get_vacancies")
    kb.adjust(1)
    return kb.as_markup()