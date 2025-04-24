import logging
import aiohttp
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.admin.schemas import EventModel, MemeberStatusModel, PeriodModel, CoordinateModel, OrganizationModel, VacancyModel, \
ScheduleModel, MainVacancyCompetencyModel, DesirableVacancyCompetencyModel, PersonalQualityModel, ProfessionModel

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

async def create_vacancy_model_from_json(python_obj) -> VacancyModel:
    value = VacancyModel (
        name=python_obj["name"],
        employment_type=python_obj["employmentType"]["name"] if python_obj["employmentType"] else None,
        experience=python_obj["experience"]["name"] if python_obj["experience"] else None,
        education_level=python_obj["educationLevel"]["name"] if python_obj["educationLevel"] else None,
        salary_from=python_obj["salaryFrom"],
        salary_up_to=python_obj["salaryUpTo"],
        before_tax=python_obj["beforeTax"],
        description=python_obj["description"],
        email=python_obj["email"],
        contact_name=python_obj["contactName"],
        phone=python_obj["phone"],
        address=python_obj["address"]["name"] if python_obj["address"] else None,
        is_blocked=python_obj["isBlocked"],
        published_at=python_obj["publishedAt"],
        is_favorite=python_obj["isFavorite"],
        hh_url=python_obj["hhUrl"]
    )
    return value

async def create_organization_model_from_json(vacancy_id, python_obj) -> OrganizationModel:
    value = OrganizationModel (
        vacancy_id=vacancy_id,
        full_title=python_obj["organization"]["fullTitle"] if python_obj["organization"] else None,
        full_title_eng=python_obj["organization"]["fullTitleEng"] if python_obj["organization"] else None,
        short_title=python_obj["organization"]["shortTitle"] if python_obj["organization"] else None,
        short_title_eng=python_obj["organization"]["shortTitleEng"] if python_obj["organization"] else None,
        description=python_obj["organization"]["description"] if python_obj["organization"] else None,
        description_eng=python_obj["organization"]["descriptionEng"] if python_obj["organization"] else None,
        supervisor_fio=python_obj["organization"]["supervisorFio"] if python_obj["organization"] else None,
        supervisor_fio_eng=python_obj["organization"]["supervisorFioEng"] if python_obj["organization"] else None,
        supervisor_job_title=python_obj["organization"]["supervisorFioEng"] if python_obj["organization"] else None,
        supervisor_job_title_eng=python_obj["organization"]["supervisorJobTitleEng"] if python_obj["organization"] else None,
        status=python_obj["organization"]["status"] if python_obj["organization"] else None,
        is_participant=python_obj["organization"]["isParticipant"] if python_obj["organization"] else None,
        is_published=python_obj["organization"]["isPublished"] if python_obj["organization"] else None,
        inn=python_obj["organization"]["inn"] if python_obj["organization"] else None,
        ogrn=python_obj["organization"]["ogrn"] if python_obj["organization"] else None,
        address_organization=python_obj["organization"]["address"] if python_obj["organization"] else None,
        address_eng=python_obj["organization"]["addressEng"] if python_obj["organization"] else None,
        phone=python_obj["organization"]["phone"] if python_obj["organization"] else None,
        email=python_obj["organization"]["email"] if python_obj["organization"] else None,
        vk=python_obj["organization"]["vk"] if python_obj["organization"] else None,
        telegram=python_obj["organization"]["telegram"] if python_obj["organization"] else None,
        site=python_obj["organization"]["site"] if python_obj["organization"] else None,
        cover=python_obj["organization"]["cover"] if python_obj["organization"] else None,
        created_vacancy_at=python_obj["organization"]["createdAt"] if python_obj["organization"] else None,
        updated_vacancy_at=python_obj["organization"]["updatedAt"] if python_obj["organization"] else None,
        published_at=python_obj["organization"]["publishedAt"] if python_obj["organization"] else None,
        licenze=(python_obj["organization"]["licenze"]["url"] if python_obj["organization"]["licenze"] else None) if python_obj["organization"] else None,
        accreditation_certificate=(python_obj["organization"]["accreditationCertificate"]["url"] if python_obj["organization"]["accreditationCertificate"] else None) if python_obj["organization"] else None,
        educational_type=(python_obj["organization"]["educationalType"]["url"] if python_obj["organization"]["educationalType"] else None) if python_obj["organization"] else None,
        is_educational=python_obj["organization"]["isEducational"] if python_obj["organization"] else None,
        is_head=python_obj["organization"]["isHead"] if python_obj["organization"] else None,
        logo=python_obj["logo"]["url"] if python_obj["logo"] else None,
        stie=python_obj["site"],
        name=python_obj["name"],
        address=python_obj["address"]
    )

    return value


async def create_schedule_model_from_json(vacancy_id, python_obj) -> List[ScheduleModel]:
    list_value = []

    for schedule in python_obj["schedule"]:
        value = ScheduleModel(
            name=schedule["name"],
            vacancy_id=vacancy_id
        )
        list_value.append(value)
    return list_value

async def create_main_vacancy_competency_model_from_json(vacancy_id, python_obj) -> List[MainVacancyCompetencyModel]:
    list_value = []

    for schedule in python_obj["mainVacancyCompetencies"]:
        value = ScheduleModel(
            name=schedule["name"],
            vacancy_id=vacancy_id
        )
        list_value.append(value)
    return list_value

async def create_desirable_vacancy_competency_model_from_json(vacancy_id, python_obj) -> List[DesirableVacancyCompetencyModel]:
    list_value = []

    for schedule in python_obj["desirableVacancyCompetencies"]:
        value = ScheduleModel(
            name=schedule["name"],
            vacancy_id=vacancy_id
        )
        list_value.append(value)
    return list_value

async def create_personal_qualities_model_from_json(vacancy_id, python_obj) -> List[PersonalQualityModel]:
    list_value = []

    for schedule in python_obj["personalQualities"]:
        value = ScheduleModel(
            name=schedule["name"],
            vacancy_id=vacancy_id
        )
        list_value.append(value)
    return list_value

async def create_profession_model_from_json(vacancy_id, python_obj) -> List[ProfessionModel]:
    list_value = []

    for schedule in python_obj["professions"]:
        value = ScheduleModel(
            name=schedule["name"],
            vacancy_id=vacancy_id
        )
        list_value.append(value)
    return list_value