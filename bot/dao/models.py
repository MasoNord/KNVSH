import datetime

from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, String, Double, DateTime
from bot.dao.database import Base


class User(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username='{self.username}')>"

class Event(Base):
    __tablename__ = "event"
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
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    member_status_name_eng: Mapped[str] = mapped_column(String, nullable=False)
    member_status_name: Mapped[str] = mapped_column(String, nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))

class OrganizerPhone(Base):
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))

class Period(Base):
    id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement='auto')
    lower: Mapped[str] = mapped_column(String, nullable=False)
    upper: Mapped[str] = mapped_column(String, nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))

class Coordinate(Base):
    id: Mapped[int] = mapped_column(BigInteger, nullable=False, primary_key=True, autoincrement='auto')
    longitude: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[str] = mapped_column(String, nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))


# class Vacancy(Base):
#     id: Mapped[int] = mapped_column(BigInteger, nullable=False, primary_key=True, autoincrement='auto')