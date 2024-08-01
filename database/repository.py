from abc import ABC, abstractmethod
from typing import Optional, Any

from sqlalchemy import select

from database.engine import async_session_maker
from database.models import Users


class AlchemyDataObject:
    def __init__(self, keys, values):
        for key, value in zip(keys, values):
            setattr(self, key, value)


class AbstractRepository(ABC):
    @abstractmethod
    async def get_one_by_filed(self, data: str, field_filter: Any):
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_filed(self, data: str, field_filter: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_one_by_fileds(self, data: list[str], field_filter: dict):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: None

    async def get_one_by_filed(self, data: str, field_filter: dict):
        async with async_session_maker() as session:
            query = select(getattr(self.model, data))
            for key, value in field_filter.items():
                query = query.filter(getattr(self.model, key) == value)
            res = await session.execute(query)
            return res.scalar()

    async def get_one_by_fileds(self, data: list[str], field_filter: dict):
        async with async_session_maker() as session:
            query = select(*[getattr(self.model, field) for field in data])
            for key, value in field_filter.items():
                query = query.filter(getattr(self.model, key) == value)
            res = await session.execute(query)
            res_values = [el._data for el in res.fetchall()]
            return [AlchemyDataObject(data, value) for value in res_values]

    async def get_all_by_filed(self, data: str, field_filter: dict):
        async with async_session_maker() as session:
            query = select(getattr(self.model, data))
            for key, value in field_filter.items():
                query = query.filter(getattr(self.model, key) == value)
            res = await session.execute(query)
            return res.scalars().all()




