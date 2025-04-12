import logging
from typing import List, Any, TypeVar, Generic
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from bot.dao.database import Base
from bot.dao.models import User


T = TypeVar("T", bound=Base)

class BaseDAO(Generic[T]):
    model: type[T]

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: BaseModel | None = None):

        # Находжение всех записей по фильтрам
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        logging.info(f"Поисх всех записей {cls.model.__name__} по фильтрам: {filter_dict}")
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            logging.info(f"Найдено {len(records)} записей")
            return records
        except SQLAlchemyError as e:
            logging.error(f"Ошибка при поиске всех записей по фильтрам {filter_dict}: {e}")
            raise
    
    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        logging.info(f"Поиск одной записи {cls.model.__name__} по фильтрам {filter_dict}")
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logging.info(f"Запись найдена по фильтрам: {filter_dict}")
            else:
                logging.info(f"Запись не найдена по фильтрам: {filter_dict}")
            return record
        except SQLAlchemyError as e:
            logging.error(f"Ошибка при поиске записи по фильтрам {filter_dict}: {e}")
            raise

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        logging.info(f"Добавление записи {cls.model.__name__} с параметрами: {values_dict}")
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            await session.flush()
            logging.info(f"Запись {cls.model.__name__} успешно добавлена.")
        except SQLAlchemyError as e:
            await session.rollback()
            logging.error(f"Ошибка при добавлении записи: {e}")
            raise e
        return new_instance

class UserDAO(BaseDAO[User]):
    model = User