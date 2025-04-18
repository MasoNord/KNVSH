from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from bot.admin.utils import process_del_text_message
from bot.dao.dao import UserDAO, EventDAO
from bot.user.schemas import TelegramIDModel, UserModel
from bot.user.kbs import main_user_kb, get_events_kb
from bot.dao.models import Event

user_router = Router()
adjust_events = []

@user_router.message(CommandStart())
async def cmd_start(message: Message, session_with_commit: AsyncSession):
    user_id = message.from_user.id
    message.delete()
    user_info = await UserDAO.find_one_or_none(
        session = session_with_commit,
        filters = TelegramIDModel(telegram_id=user_id)
    )

    if user_info:
        return await message.answer(
            f"👋 Привет, {message.from_user.full_name}! Выберите необходимое действие",
            reply_markup=main_user_kb(user_id)
        )
    
    values = UserModel (
        telegram_id = user_id,
        username = message.from_user.username,
        first_name = message.from_user.first_name,
        last_name = message.from_user.last_name
    )

    await UserDAO.add(session = session_with_commit, values=values)
    await message.answer(f"🎆🎇🎈🎉 <b>Благодарим за регистрацию!</b> Теперь выберите необходимое действие.",
                         reply_markup=main_user_kb(user_id))
    
@user_router.callback_query(F.data == "home")
async def home(call: CallbackQuery):
    user_id = call.from_user.id
    await call.message.delete()
    await call.message.answer (
        text="Выберите необходимое действие",
        reply_markup=main_user_kb(user_id)
    )

@user_router.callback_query(F.data == "get_events")
async def get_events(call: CallbackQuery, session_with_commit: AsyncSession, current_index: int):
    await call.message.delete()
    events = await EventDAO.find_all(session=session_with_commit, filters=None)
    temp = []
    for event in events:
        if len(temp) == 5:
            adjust_events.append(temp)
            temp = []
        else:
            temp.append(event.title)
    
    if len(temp) != 0: adjust_events.append(temp)
    await call.message.answer(
        text = "Список доступных мероприятий",
        reply_markup=get_events_kb(events=adjust_events, start=current_index)
    )

@user_router.callback_query(F.data == "forward_to_list")
async def forward_to_list(call: CallbackQuery, current_index: int):
    await call.message.delete()
    if (current_index + 1) != len(adjust_events):
        current_index += 1

    await call.message.answer(
        text = "Список доступных мероприятий",
        reply_markup=get_events_kb(events=adjust_events, start=current_index)
    )

@user_router.callback_query(F.data == "back_to_list")
async def back_to_list(call: CallbackQuery, current_index: int):
    await call.message.delete()
    if (current_index - 1) != -1:
        current_index -= 1

    await call.message.answer(
        text = "Список доступных мероприятий",
        reply_markup=get_events_kb(events=adjust_events, start=current_index)
    )

# @user_router.callback_query(F.data == "back_to_list_denied")
# async def back_to_list_denied(call: CallbackQuery, current_index: int):
#     await call.answer("Доступ назад ограничен")
#     await call.message.answer(
#         text = "Список доступных мероприятий",
#         reply_markup=get_events_kb(events=adjust_events, start=current_index)
#     )

# @user_router.callback_query(F.data == "forward_to_list_denied")
# async def back_to_list_denied(call: CallbackQuery, current_index: int):
#     await call.answer("Доступ вперед ограничен")
#     await call.message.answer(
#         text = "Список доступных мероприятий",
#         reply_markup=get_events_kb(events=adjust_events, start=current_index)
#     )