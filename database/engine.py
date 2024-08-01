import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from database.config import load_config

config = load_config()
engine = create_async_engine(config.db.construct_sqlalchemy_url())
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_async_session_maker():
    async with async_session_maker() as session:
        yield session

