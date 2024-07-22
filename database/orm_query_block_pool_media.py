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
