from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from bot.admin.utils import process_del_text_message
from bot.dao.dao import UserDAO, EventDAO, VacancyDAO, OrganizationDAO
from bot.user.schemas import TelegramIDModel, UserModel
from bot.admin.schemas import EventModelTitle, VacancyModelName, OrganizationModelVacancyId
from bot.user.kbs import main_user_kb, get_events_kb, get_vacancies_kb, back_to_event_list, back_to_vacancys_list
from bot.config import settings
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
        if len(temp) == settings.MAX_ENTITIES_IN_GET_KEYBOARDS:
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
        if len(temp) == settings.MAX_ENTITIES_IN_GET_KEYBOARDS:
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

@user_router.callback_query(F.data.startswith("get_event_by_"))
async def get_event(call: CallbackQuery, session_with_commit: AsyncSession):
    await call.message.delete()
    key = display.adjust_events[display.current_event_index][int(call.data.split('_')[3])]
    event = await EventDAO.find_one_or_none(session=session_with_commit, filters=EventModelTitle(title=key))

    msg = ""
    if event.cover_url:
        msg = "https://researchinspb.ru" + event.cover_url + "\n"
    
    msg += f"""
<b>{event.title}</b>\n
<b>Адрес:</b> {event.location}
<b>Организатор:</b> {event.organizer}
<b>Формат:</b> {event.event_format}
<b>Статус:</b> {event.status}
<b>Тип:</b> {event.typeof}
    """
    
    await call.message.answer(
        text=msg,
        reply_markup=back_to_event_list()
    )

@user_router.callback_query(F.data.startswith("get_vacancy_by_"))
async def get_vacancy(call: CallbackQuery, session_with_commit: AsyncSession):
    await call.message.delete()
    index = call.data.split('_')[3]
    logging.info(index)
    
    key = display.adjust_vacancies[display.current_vacancy_index][int(index)]
    vacancy = await VacancyDAO.find_one_or_none(session=session_with_commit, filters=VacancyModelName(name=key))
    organization = await OrganizationDAO.find_one_or_none(session=session_with_commit, filters=OrganizationModelVacancyId(vacancy_id=vacancy.id))


    msg = f"""
<b>{vacancy.name}</b>\n
<b>Тип Занятости:</b> {vacancy.employment_type}
<b>Опыт Работы:</b> {vacancy.experience}
<b>Образование:</b> {vacancy.education_level}
<b>Зарплата:</b> {f"От {vacancy.salary_from}" if vacancy.salary_from else ""} {f"До {vacancy.salary_up_to}" if vacancy.salary_up_to else ""}
<b>До Налогов:</b> {"Да" if vacancy.before_tax else "Нет"}
<b>Cайт:</b> {organization.site if organization.site else ""}
<b>HHru:</b> {vacancy.hh_url}
    """
    await call.message.answer(
        text=msg,
        reply_markup=back_to_vacancys_list()
    )