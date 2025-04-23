import logging
import aiohttp
import json
from typing import List
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.admin.schemas import EventModel, MemeberStatusModel, PeriodModel, CoordinateModel

from bot.config import bot

async def process_del_text_message(message: Message, state: FSMContext):
    data = await state.get_data()
    last_msg_id = data.get('last_msg_id')

    try:
        if last_msg_id:
            await bot.delete_message(chat_id=message.from_user.id, message_id=last_msg_id)
        else:
            logging.warning("Ошибка: Не удалось найти идентификатор последнего сообщения для удаления.")
        await message.delete()
    except Exception as e:
        logging.error(f"Произошла ошибка при удалении сообщения: {str(e)}")


async def proecess_get_url_request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url['url']) as response:
                if response.status == 404 or response.status == 500:
                    return None
                html = await response.text()
                python_obj = json.loads(html)
        except aiohttp.client_exceptions.InvalidUrlClientError:
            return None

    return python_obj

async def create_event_model_from_json(python_obj) -> EventModel:
    value = EventModel (
        isFavorite=python_obj['isFavorite'],
        organizer=python_obj['organizer']['name'] if python_obj['organizer'] is not None else None,
        organizer_address=python_obj['organizerAddress'],
        organizer_address_eng=python_obj['organizerAddressEng'],
        organizer_supervisor_fio=python_obj['organizerSupervisorFio'],
        organizer_supervisor_fio_eng=python_obj['organizerSupervisorFioEng'],
        organizer_site=python_obj['organizerSite'],
        organizer_vk=python_obj['organizerVk'],
        organizer_telegram=python_obj['organizerTelegram'],
        organizer_email=python_obj['organizerEmail'],
        free_places=python_obj['freePlaces'],
        event_type=python_obj['type']['name'] if python_obj['type'] is not None else None,
        is_active=python_obj['isActive'],
        event_format=python_obj['eventFormat']['name'] if python_obj['eventFormat'] is not None else None,
        status=python_obj['status']['name'] if python_obj['status'] is not None else None,
        location=python_obj['location'],
        location_eng=python_obj['locationEng'],
        registration_status=python_obj['registrationStatus']['name'] if python_obj['registrationStatus'] is not None else None,
        registration_comment=python_obj['registrationComment'],
        place_number=python_obj['placesNumber'],
        is_available=python_obj['isAvailable'],
        title=python_obj['title'],
        title_eng=python_obj['titleEng'],
        cypher=python_obj['cypher'],
        published_at=python_obj['publishedAt'],
        cover_url=python_obj['cover']['url'] if python_obj['cover'] is not None else None,
        parent=python_obj['parent'],
        typeof=python_obj['typeof']['name'] if python_obj['typeof'] is not None else None
    )

    return value

async def create_memeber_status_model_from_json(python_obj, event_id) -> List[MemeberStatusModel]:
    list_value = []

    for value in python_obj['membersStatuses']:
        member = MemeberStatusModel(
            member_status_name_eng=value["id"],
            member_status_name=value["name"],
            event_id=event_id
        )

        list_value.append(member)
    
    return list_value

async def create_period_mode_from_json(python_obj, event_id) -> List[PeriodModel]:
    list_value = []

    for value in python_obj['periods']:
        period = PeriodModel (
            lower=value['lower'],
            upper=value['upper'],
            event_id=event_id
        )
        list_value.append(period)

    return list_value

async def create_coordinate_model_from_json(python_obj, event_id) -> List[CoordinateModel]:
    list_value = []

    for value in python_obj['coordinates']:
        coord = CoordinateModel(
            longitude=str(value[0]),
            latitude=str(value[1]),
            event_id=event_id
        )
        list_value.append(coord)

    return list_value
