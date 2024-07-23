import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Block, BlockPool, MediaBlockPool
from sqlalchemy import select, update


async def add_block_pool_media(session: AsyncSession, **kwargs):
    obj = MediaBlockPool(
        block_pool_id=kwargs.get("block_pool_id"),
        photo_id=kwargs.get("photo_id"),
        video_id=kwargs.get("video_id"),
    )
    session.add(obj)
    await session.commit()


async def get_videos_id_from_block_pool_session_pool(session_pool, **kwargs):
    query = select(MediaBlockPool.video_id).where((MediaBlockPool.block_pool_id == kwargs.get("block_pool_id"))
                                     & (MediaBlockPool.video_id != None))
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()


async def get_videos_id_from_block_pool(session, **kwargs):
    query = select(MediaBlockPool.video_id).where((MediaBlockPool.block_pool_id == kwargs.get("block_pool_id"))
                                     & (MediaBlockPool.video_id != None))
    result = await session.execute(query)
    return result.fetchall()


async def get_photos_id_from_block_pool_session_pool(session_pool, **kwargs):
    query = select(MediaBlockPool.photo_id).where((MediaBlockPool.block_pool_id == kwargs.get("block_pool_id"))
                                     & (MediaBlockPool.photo_id != None))
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()


async def get_photos_id_from_block_pool(session, **kwargs):
    query = select(MediaBlockPool.photo_id).where((MediaBlockPool.block_pool_id == kwargs.get("block_pool_id"))
                                     & (MediaBlockPool.photo_id != None))
    result = await session.execute(query)
    return result.fetchall()
