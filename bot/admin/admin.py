from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from bot.config import admins
from bot.admin.kbs import admin_kb, add_events_kb, cancel_kb_inline
from bot.admin.utils import proecess_get_url_request, create_event_model_from_json, create_period_mode_from_json, create_memeber_status_model_from_json, create_coordinate_model_from_json
from bot.dao.dao import EventDAO, MemeberStatusDAO, CoordinateDAO, PeriodDAO

admin_router = Router()

class AddEvets(StatesGroup):
    url = State()


@admin_router.callback_query(F.data == "admin_panel", F.from_user.id.in_(admins))
async def start_admin(call: CallbackQuery):
    await call.answer('Доступ в админ-панель разрешен!')
    await call.message.edit_text(
        text="Вам разрешен доступ в админ-панель. Выберите необходимое действие.",
        reply_markup=admin_kb()
    )

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
    
    while True:
        values = python_obj['results']
        for value in values:
            event = await create_event_model_from_json(value)
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

        if python_obj['next'] is not None:
            python_obj = await proecess_get_url_request(python_obj['next'])
        else:
            break

    await message.answer (
        text=f"Спасибо большое запредоставленный {url}",
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