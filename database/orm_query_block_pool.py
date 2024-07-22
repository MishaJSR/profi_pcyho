import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Block, BlockPool
from sqlalchemy import select, update


async def add_block_pool(session: AsyncSession, **kwargs):
    obj = BlockPool(
        block_main_id=kwargs.get("block_main_id"),
        content=kwargs.get("content"),
        has_media=kwargs.get("has_media")
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj.id


async def get_block_pool_all_session_pool(session_pool, **kwargs):
    query = select(BlockPool).where(BlockPool.block_main_id == kwargs.get("block_main_id"))
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()
