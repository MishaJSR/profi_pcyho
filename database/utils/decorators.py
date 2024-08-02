from sqlalchemy import select

from database.engine import async_session_maker


def async_session_maker_decorator(func):
    async def wrapper(self_object, **kwargs):
        async with async_session_maker() as session:
            query = select(*[getattr(self_object.model, field) for field in kwargs.get("data")])
            for key, value in kwargs.get("field_filter").items():
                query = query.filter(getattr(self_object.model, key) == value)
            res = await session.execute(query)
            return await func(self_object, data=kwargs.get("data"), result_query=res)

    return wrapper
