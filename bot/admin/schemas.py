
from pydantic import BaseModel, Field, ConfigDict
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
