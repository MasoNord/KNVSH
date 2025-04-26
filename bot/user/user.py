from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from bot.admin.utils import process_del_text_message
from bot.dao.dao import UserDAO, EventDAO, VacancyDAO
from bot.user.schemas import TelegramIDModel, UserModel
from bot.user.kbs import main_user_kb, get_events_kb, get_vacancies_kb
from bot.dao.models import Event
from bot.user.utils import DisplayObjects
import logging

user_router = Router()
display = DisplayObjects(adjust_vacancies=[], adjust_events=[], current_event_index=0, current_vacancy_index=0)


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
async def get_events(call: CallbackQuery, session_with_commit: AsyncSession):
    user_id = call.from_user.id
    await call.message.delete()
    display.adjust_events.clear()

    events = await EventDAO.find_all(session=session_with_commit, filters=None)
    temp = []

    for event in events:
        if len(temp) == 5:
            display.adjust_events.append(temp)
            temp = []
        else:
            temp.append(event.title)
    
    if len(temp) != 0: display.adjust_events.append(temp)

    if len(display.adjust_events) == 0:
        await call.message.answer(
            text="Упс! Походу на данный момент нет активных мероприятий, попрбуйте посмотреть позже!",
            reply_markup=main_user_kb(user_id)
        )

    await call.message.answer(
        text = "Список доступных мероприятий",
        reply_markup=get_events_kb(events=display.adjust_events, start=display.current_event_index)
    )

@user_router.callback_query(F.data == "forward_to_list_events")
async def forward_to_list(call: CallbackQuery):
    await call.message.delete()
    if (display.current_event_index + 1) < len(display.adjust_events):
        display.current_event_index += 1

    await call.message.answer(
        text = "Список доступных мероприятий",
        reply_markup=get_events_kb(events=display.adjust_events, start=display.current_event_index)
    )

@user_router.callback_query(F.data == "back_to_list_events")
async def back_to_list(call: CallbackQuery):
    await call.message.delete()

    if (display.current_event_index - 1) > -1:
        display.current_event_index -= 1

    await call.message.answer(
        text = "Список доступных мероприятий",
        reply_markup=get_events_kb(events=display.adjust_events, start=display.current_event_index)
    )

@user_router.callback_query(F.data == "get_vacancies")
async def get_vacancies(call: CallbackQuery, session_with_commit: AsyncSession):
    user_id = call.from_user.id
    await call.message.delete()

    display.adjust_vacancies.clear()

    vacancies = await VacancyDAO.find_all(session=session_with_commit, filters=None)
    temp = []
    for vacancy in vacancies:
        if len(temp) == 5:
            display.adjust_vacancies.append(temp)
            temp = []
        else:
            if vacancy.name not in display.adjust_vacancies:
                temp.append(vacancy.name)
    
    if len(temp) != 0: display.adjust_vacancies.append(temp)

    if len(display.adjust_vacancies) == 0:
        await call.message.answer(
            text="Упс! Походу на данный момент нет активных вакансий, попрбуйте посмотреть позже!",
            reply_markup=main_user_kb(user_id)
        )

    await call.message.answer(
        text = "Список доступных мероприятий",
        reply_markup=get_vacancies_kb(vacancies=display.adjust_vacancies, start=display.current_vacancy_index)
    )

@user_router.callback_query(F.data == "forward_to_list_vacancies")
async def forward_to_list(call: CallbackQuery):
    await call.message.delete()
    if (display.current_vacancy_index + 1) != len(display.adjust_vacancies):
        display.current_vacancy_index += 1

    await call.message.answer(
        text = "Список доступных мероприятий",
        reply_markup=get_vacancies_kb(vacancies=display.adjust_vacancies, start=display.current_vacancy_index)
    )

@user_router.callback_query(F.data == "back_to_list_vacancies")
async def back_to_list(call: CallbackQuery):
    await call.message.delete()
    if (display.current_vacancy_index - 1) != -1:
        display.current_vacancy_index -= 1

    await call.message.answer(
        text = "Список доступных мероприятий",
        reply_markup=get_vacancies_kb(vacancies=display.adjust_vacancies, start=display.current_vacancy_index)
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