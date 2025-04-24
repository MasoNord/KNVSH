
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
import datetime

class EventModelTitle(BaseModel):
    title: str | None
    model_config = ConfigDict(from_attributes=True)

class OrganizerPhoneModelID(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class PeriodModelID(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class CoordinateModelID(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class EventModel(EventModelTitle):
    isFavorite: bool | None
    organizer: str | None
    organizer_address: str | None
    organizer_address_eng: str | None
    organizer_supervisor_fio: str | None
    organizer_supervisor_fio_eng: str | None
    organizer_site: str | None
    organizer_vk: str | None
    organizer_telegram: str | None
    organizer_email: str | None
    free_places: bool | None
    is_active: bool | None
    event_type: str | None
    event_format: str | None
    status: str | None
    location: str | None
    location_eng: str | None
    registration_status: str | None
    # registration_period: str | None
    registration_comment: str | None
    place_number: str | None
    is_available: bool | None
    # title: str | None
    title_eng: str | None
    cypher: str | None
    published_at: str | None
    cover_url: str | None
    parent: bool | None
    typeof: str | None

class MemeberStatusModel(BaseModel):
    member_status_name_eng: str
    member_status_name: str
    event_id: int | None

class OrganizerPhoneModel(OrganizerPhoneModelID):
    phone_number: str
    event_id: int | None

class PeriodModel(PeriodModelID):
    lower: str
    upper: str
    event_id: int | None

class CoordinateModel(CoordinateModelID):
    longitude: str
    latitude: str
    event_id: int | None

class VacancyModelName(BaseModel):
    name: str

class VacancyModel(BaseModel):
    name: str
    employment_type: str | None
    experience: str | None
    education_level: str | None
    salary_from: int | None
    salary_up_to: int | None
    before_tax: bool
    description: str
    email: str | None
    contact_name: str | None
    phone: str | None
    address: str | None
    is_blocked: bool
    published_at: str
    is_favorite: bool
    hh_url: str | None
    

class OrganizationModel(BaseModel):
    vacancy_id: int | None
    full_title: str | None
    full_title_eng: str | None
    short_title: str | None
    short_title_eng: str | None
    description: str | None
    description_eng: str | None
    supervisor_fio: str | None
    supervisor_fio_eng: str | None
    supervisor_job_title: str | None
    supervisor_job_title_eng: str | None
    status: bool | None
    is_participant: bool | None
    is_published: bool | None
    inn: str | None
    ogrn: str | None
    address_organization: str | None
    address_eng: str | None
    phone: str | None
    email: str | None
    vk: str | None
    telegram: str | None
    site: str | None
    logo: str | None
    cover: str | None
    created_vacancy_at: str | None
    updated_vacancy_at: str | None
    published_at: str | None
    licenze: str | None
    accreditation_certificate: str | None
    educational_type: str | None
    is_educational: bool | None
    is_head: bool | None
    logo: str | None
    stie: str | None
    name: str | None
    address: str | None

class ScheduleModel(BaseModel):    
    vacancy_id: int 
    name: str

class MainVacancyCompetencyModel(BaseModel):
    vacancy_id: int 
    name: str

class DesirableVacancyCompetencyModel(BaseModel):
    vacancy_id: int
    name: str

class PersonalQualityModel(BaseModel):
    vacancy_id: int
    name: str

class ProfessionModel(BaseModel):
    vacancy_id: int
    name: str