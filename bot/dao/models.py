from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, String, Double, DateTime, Column, Table
from bot.dao.database import Base


# --------------------------------------------- Модели для мероприятий ---------------------------------------------

class User(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username='{self.username}')>"

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    isFavorite: Mapped[bool | None]
    organizer: Mapped[str | None]
    organizer_address: Mapped[str | None]
    organizer_address_eng: Mapped[str | None]
    organizer_supervisor_fio: Mapped[str | None]
    organizer_supervisor_fio_eng: Mapped[str | None]
    organizer_site: Mapped[str | None]
    organizer_vk: Mapped[str | None]
    organizer_telegram: Mapped[str | None]
    organizer_email: Mapped[str | None]
    free_places: Mapped[bool | None]
    is_active: Mapped[bool | None]
    event_type: Mapped[str | None]
    member_status_id: Mapped[List["MemeberStatus"]] = relationship()
    organizer_phone: Mapped[List["OrganizerPhone"]] = relationship()
    event_format: Mapped[str | None]
    status: Mapped[str | None]
    location: Mapped[str | None]
    location_eng: Mapped[str | None]
    registration_status: Mapped[str | None]
    registration_period: Mapped[str | None]
    registration_comment: Mapped[str | None]
    place_number: Mapped[str | None]
    periods: Mapped[List["Period"]] = relationship()
    is_available: Mapped[bool | None]
    coordinates: Mapped[List["Coordinate"]] = relationship()
    title: Mapped[str | None]
    title_eng: Mapped[str | None]
    cypher: Mapped[str | None]
    published_at: Mapped[str | None]
    cover_url: Mapped[str | None]
    parent: Mapped[bool | None]
    typeof: Mapped[str | None]

class MemeberStatus(Base):
    __tablename__ = "member_statuses"
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    member_status_name_eng: Mapped[str] = mapped_column(String, nullable=False)
    member_status_name: Mapped[str] = mapped_column(String, nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))

class OrganizerPhone(Base):
    __tablename__ = "organizer_phones"
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))

class Period(Base):
    __tablename__ = "periods"
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    lower: Mapped[str] = mapped_column(String, nullable=False)
    upper: Mapped[str] = mapped_column(String, nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))

class Coordinate(Base):
    __tablename__ = "coordinates"

    id: Mapped[int] = mapped_column(BigInteger, nullable=False, primary_key=True, autoincrement='auto')
    longitude: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[str] = mapped_column(String, nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))


# --------------------------------------------- Модели для вакансий ---------------------------------------------
class Vacancy(Base):
    __tablename__ = "vacancy"
    
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    name: Mapped[str]
    organization: Mapped["Organization"] = relationship()
    employment_type: Mapped[str]
    schedule: Mapped[List["Schedule"]] = relationship()
    experience: Mapped[str]
    education_level: Mapped[str]
    salary_from: Mapped[int | None]
    salary_up_to: Mapped[int | None]
    before_tax: Mapped[bool]
    description: Mapped[str]
    professions: Mapped[List["Profession"]] = relationship()
    main_facancy_competencies: Mapped[List["MainVacancyCompetency"]] = relationship()
    desirable_vacancy_competencies: Mapped[List["DesirableVacancyCompetency"]] = relationship()
    personal_qualities: Mapped[List["PersonalQuality"]] = relationship()
    email: Mapped[str | None]
    contact_name: Mapped[str | None]
    phone: Mapped[str | None]
    address: Mapped[str | None]
    is_blocked: Mapped[bool]
    published_at: Mapped[str]
    is_favorite: Mapped[bool]
    hh_url: Mapped[str | None]
    

class Organization(Base):
    __tablename__ = "organization"
    
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"), nullable=False)

    full_title: Mapped[str | None]
    full_title_eng: Mapped[str | None]
    short_title: Mapped[str | None]
    short_title_eng: Mapped[str | None]
    description: Mapped[str | None]
    description_eng: Mapped[str | None]
    supervisor_fio: Mapped[str | None]
    supervisor_fio_eng: Mapped[str | None]
    supervisor_job_title: Mapped[str | None]
    supervisor_job_title_eng: Mapped[str | None]
    status: Mapped[bool | None]
    is_participant: Mapped[bool | None]
    is_published: Mapped[bool | None]
    inn: Mapped[str | None]
    ogrn: Mapped[str | None]
    address_organization: Mapped[str | None]
    address_eng: Mapped[str | None]
    phone: Mapped[str | None]
    email: Mapped[str | None]
    vk: Mapped[str | None]
    telegram: Mapped[str | None]
    site: Mapped[str | None]
    logo: Mapped[str | None]
    cover: Mapped[str | None]
    created_vacancy_at: Mapped[str | None]
    updated_vacancy_at: Mapped[str | None]
    published_at: Mapped[str | None]
    licenze: Mapped[str | None]
    accreditation_certificate: Mapped[str | None]
    educational_type: Mapped[str | None]
    is_educational: Mapped[bool | None]
    is_head: Mapped[bool | None]
    logo: Mapped[str | None]
    stie: Mapped[str | None]
    name: Mapped[str | None]
    address: Mapped[str | None]

class Schedule(Base):
    __tablename__ = "schedule"
    
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"), nullable=False)
    name: Mapped[str]

class MainVacancyCompetency(Base):
    __tablename__ = "main_vacancy_competency"
    
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"), nullable=False)
    name: Mapped[str]

class DesirableVacancyCompetency(Base):
    __tablename__ = "desirable_vacancy_competency"

    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"), nullable=False)
    name: Mapped[str]

class PersonalQuality(Base):
    __tablename__ = "personal_qualities"
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"), nullable=False)
    name: Mapped[str]

class Profession(Base):
    __tablename__ = "professions"
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"), nullable=False)
    name: Mapped[str]