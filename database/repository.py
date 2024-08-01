from abc import ABC, abstractmethod

from sqlalchemy import select


class AbstractRepository(ABC):
    @abstractmethod
    async def get_one(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError


class SQLAlchlemyRepository(AbstractRepository):
    model: None

    async def get_one(self, filter):
        query = select(self.model)
        result = await session.execute(query)
        return result.scalarone()

    async def get_all(self):
        raise NotImplementedError
