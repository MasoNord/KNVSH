from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from bot.config import admins
from bot.admin.kbs import admin_kb, add_events_kb, cancel_kb_inline, continue_add_new_events, add_vacancy_kb
from bot.admin.utils import (
    proecess_get_url_request, create_event_model_from_json, create_period_mode_from_json,
    create_memeber_status_model_from_json, create_vacancy_model_from_json, create_coordinate_model_from_json,
    create_organization_model_from_json, create_schedule_model_from_json, create_main_vacancy_competency_model_from_json,
    create_desirable_vacancy_competency_model_from_json, create_personal_qualities_model_from_json, create_profession_model_from_json
) 
from bot.dao.dao import (
    EventDAO, MemeberStatusDAO, CoordinateDAO, PeriodDAO, VacancyDAO,
    OrganizationDAO, ScheduleDAO, MainVacancyCompetencyDAO, DesirableVacancyCompetencyDAO, ProfessionDAO, PersonalQualityDAO
) 
from bot.admin.schemas import EventModelTitle, VacancyModelName

admin_router = Router()

class AddEvets(StatesGroup):
    url = State()

class AddVacancy(StatesGroup):
    url = State()


@admin_router.callback_query(F.data == "admin_panel", F.from_user.id.in_(admins))
async def start_admin(call: CallbackQuery):
    await call.answer('Доступ в админ-панель разрешен!')
    await call.message.edit_text(
        text="Вам разрешен доступ в админ-панель. Выберите необходимое действие.",
        reply_markup=admin_kb()
    )

@admin_router.callback_query(F.data == "cancel", F.from_user.id.in_(admins))
async def admin_process_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.answer("Отмена сценария добавления новых ивентов")
    await call.message.delete()
    await call.message.answer(
        text="Отмена добавления ивентов",
        reply_markup=admin_kb()
    )

# ----------------------------- Добавление новых ивентов -----------------------------


@admin_router.callback_query(F.data == "add_events", F.from_user.id.in_(admins))
async def add_events(call: CallbackQuery):
    await call.message.edit_text(
        text="Для добавления новых мероприятий выберите удобный для вас способ",
        reply_markup = add_events_kb()
    )

@admin_router.callback_query(F.data == "add_events_by_url", F.from_user.id.in_(admins))
async def add_events_by_url(call: CallbackQuery, state: FSMContext):
    await call.answer("Запущен сценарий добалвения мероприятий")
    await call.message.delete()
    msg = await call.message.answer(
        text="Загрузите url ссылку c мероприятиями в json формате",
        reply_markup=cancel_kb_inline()
    )
    await state.update_data(last_msg_id=msg.message_id)
    await state.set_state(AddEvets.url)

# Метод для добаления новых ивентов через ссылку на json файл

@admin_router.message(F.text, F.from_user.id.in_(admins), AddEvets.url)
async def admin_process_add_events_by_url(message: Message, state: FSMContext,  session_with_commit: AsyncSession):
    await state.update_data(url = message.text.lower())

    url = await state.get_data()
    python_obj = await proecess_get_url_request(url)

# TODO: доделать обработку исключения на неверно введенный юрл
    if python_obj is None:
        return await message.answer(
            text="Что-то пошло не так, попробуйте загрузить ссылку еще раз, либо выбирете другую"
        )
    
    # while True:
    #     values = python_obj['results']
    #     for value in values:
    #         event = await create_event_model_from_json(value)
    #         event_instance = await EventDAO.add(session=session_with_commit, values=event)

    #         periods = await create_period_mode_from_json(value, event_instance.id)
    #         member_statuses = await create_memeber_status_model_from_json(value, event_instance.id)
    #         coordinates = await create_coordinate_model_from_json(value, event_instance.id)

    #         for period in periods:
    #             await PeriodDAO.add(session=session_with_commit, values=period)

    #         for member in member_statuses:
    #             await MemeberStatusDAO.add(session=session_with_commit, values=member)
            
    #         for coord in coordinates:
    #             await CoordinateDAO.add(session=session_with_commit, values=coord)

    #     if python_obj['next'] is not None:
    #         python_obj = await proecess_get_url_request(python_obj['next'])
    #     else:
    #         break
    
    values = python_obj['results']
    count = 0
    msg = ""
    for value in values:
        event = await create_event_model_from_json(value)

        if await EventDAO.find_one_or_none(session=session_with_commit, filters=EventModelTitle(title=event.title)):
            msg += f"Мероприятие {event.title} уже существует в базе данных\n"
            continue

        event_instance = await EventDAO.add(session=session_with_commit, values=event)

        periods = await create_period_mode_from_json(value, event_instance.id)
        member_statuses = await create_memeber_status_model_from_json(value, event_instance.id)
        coordinates = await create_coordinate_model_from_json(value, event_instance.id)

        for period in periods:
            await PeriodDAO.add(session=session_with_commit, values=period)

        for member in member_statuses:
            await MemeberStatusDAO.add(session=session_with_commit, values=member)
        
        for coord in coordinates:
            await CoordinateDAO.add(session=session_with_commit, values=coord)

        msg += f"Мероприятие {event.title} успешно было доавблено в базу\n"
        count += 1
    msg += f"Всего добавлнео {count} новых мероприятий"
    
    await message.answer (
        text=msg,
        reply_markup=continue_add_new_events()
    )



# ----------------------------- Добавление новых вакансий -----------------------------

@admin_router.callback_query(F.data == "add_vacancies", F.from_user.id.in_(admins))
async def add_events(call: CallbackQuery):
    await call.message.edit_text(
        text="Для добавления новых вакансий выберите удобный для вас способ",
        reply_markup = add_vacancy_kb()
    )

@admin_router.callback_query(F.data == "add_vacancies_by_url", F.from_user.id.in_(admins))
async def add_events_by_url(call: CallbackQuery, state: FSMContext):
    await call.answer("Запущен сценарий добалвения мероприятий")
    await call.message.delete()
    msg = await call.message.answer(
        text="Загрузите url ссылку c вакансиями в json формате",
        reply_markup=cancel_kb_inline()
    )
    await state.update_data(last_msg_id=msg.message_id)
    await state.set_state(AddVacancy.url)


@admin_router.message(F.text, F.from_user.id.in_(admins), AddVacancy.url)
async def admin_process_add_events_by_url(message: Message, state: FSMContext,  session_with_commit: AsyncSession):
    await state.update_data(url = message.text.lower())

    url = await state.get_data()
    python_obj = await proecess_get_url_request(url)

# TODO: доделать обработку исключения на неверно введенный юрл
    if python_obj is None:
        return await message.answer(
            text="Что-то пошло не так, попробуйте загрузить ссылку еще раз, либо выбирете другую"
        )
    
    values = python_obj['results']
    count = 0
    msg = ""


    for value in values:
        print(value["address"])

        vacancy = await create_vacancy_model_from_json(value)
        if await VacancyDAO.find_one_or_none(session=session_with_commit, filters=VacancyModelName(name=vacancy.name)):
            msg += f"Вакансия {vacancy.name} уже существует в базе данных\n"
            continue

        vacancy_instance = await VacancyDAO.add(session=session_with_commit, values=vacancy)

        organization = await create_organization_model_from_json(vacancy_instance.id, value["organization"])
        schedule = await create_schedule_model_from_json(vacancy_instance.id, value)
        main_vacancy_competency = await create_main_vacancy_competency_model_from_json(vacancy_instance.id, value)
        desirable_vacancy_competency = await create_desirable_vacancy_competency_model_from_json(vacancy_instance.id, value)
        personal_qualities = await create_personal_qualities_model_from_json(vacancy_instance.id, value)
        profession = await create_profession_model_from_json(vacancy_instance.id, value)

        await OrganizationDAO.add(session=session_with_commit, values=organization)
        
        for sc in schedule:
            await ScheduleDAO.add(session=session_with_commit, values=sc)
        
        for mvc in main_vacancy_competency:
            await MainVacancyCompetencyDAO.add(session=session_with_commit, values=mvc)

        for dvc in desirable_vacancy_competency:
            await DesirableVacancyCompetencyDAO.add(session=session_with_commit, values=dvc)

        for pq in personal_qualities:
            await PersonalQualityDAO.add(session=session_with_commit, values=pq)

        for pr in profession:
            await ProfessionDAO.add(session=session_with_commit, values=pr)
        
        msg += f"Мероприятие {vacancy.name} успешно было доавблено в базу\n"
        count += 1
    
    msg += f"Всего добавлнео {count} новых мероприятий"

    await message.answer (
        text=msg,
        reply_markup=continue_add_new_events()
    )

