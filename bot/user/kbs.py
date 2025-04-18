from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

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
    # keyboards = []
    # temp = []

    # for i in range(len(events)):
    #     if len(temp) == 5:
    #         keyboards.append(temp)
    #         temp = []
    #     else:
    #         temp.append(events[i])
        

    # for i in range(keyboards[start]):
    #     adjust_elements.append(1)
    #     kb.button(text=keyboards[start][i].title, callback_data=f"get_event_by_{i}")

    adjust_elements = []
    for i in range(len(events)):
        adjust_elements.append(1)
        kb.button(text=f"{events[i].title}", callback_data=f"get_event_by_{i}")

    adjust_elements.append(3)
    kb.button(text="⬅️", callback_data="back_to_list")
    kb.button(text=f"{start}/{len(events)}", callback_data="reminder")
    kb.button(text="➡️", callback_data="forward_to_list")
    adjust_elements.append(1)
    kb.button(text="🏠 На главную", callback_data="home")

    kb.adjust(*adjust_elements,3)
    return kb.as_markup()