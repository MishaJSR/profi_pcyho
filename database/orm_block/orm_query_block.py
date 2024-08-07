import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Block
from sqlalchemy import select, update


async def add_block(session: AsyncSession, **kwargs):
    obj = Block(
        block_name=kwargs.get("block_name"),
        content=kwargs.get("content"),
        has_media=kwargs.get("has_media"),
        date_to_post=kwargs.get("date_to_post"),
        progress_block=kwargs.get("progress_block"),
        callback_button_id=kwargs.get("callback_button_id"),
        is_vebinar=kwargs.get("is_vebinar"),
        is_sub_block=kwargs.get("is_sub_block")
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj.id


async def get_block_for_add_task(session: AsyncSession, **kwargs):
    query = select(Block).where((Block.is_visible == True) & (Block.is_vebinar == False)).order_by(Block.date_to_post)
    result = await session.execute(query)
    return result.fetchall()


#


async def get_block_for_delete(session: AsyncSession, **kwargs):
    query = select(Block).where((Block.is_visible == True)).order_by(Block.date_to_post)
    result = await session.execute(query)
    return result.scalars().all()


async def get_block_active(session: AsyncSession, **kwargs):
    query = select(Block).where(Block.is_visible == True).order_by(Block.date_to_post)
    result = await session.execute(query)
    return result.scalars().all()


async def get_block_id_by_callback(session: AsyncSession, **kwargs):
    query = select(Block.id).where((Block.is_visible == True) & (Block.is_vebinar == False) & (
            Block.callback_button_id == kwargs.get("callback_button_id")))
    result = await session.execute(query)
    return result.fetchone()


async def get_block_session_pool_by_id(session_pool, **kwargs):
    query = select(Block).where(
        (Block.is_visible == True) & (Block.is_vebinar == False) & (Block.id == kwargs.get("block_id")))
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchone()

async def get_block_session_by_id(session, **kwargs):
    query = select(Block).where(
        (Block.is_visible == True) & (Block.is_vebinar == False) & (Block.id == kwargs.get("block_id")))
    result = await session.execute(query)
    return result.fetchone()


async def get_block_all_session_pool(session_pool, **kwargs):
    query = select(Block).where(Block.is_visible == True)
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()

async def get_block_all_session(session, **kwargs):
    query = select(Block).where(Block.is_visible == True)
    result = await session.execute(query)
    return result.fetchall()


async def get_block_names_all_not_past(session: AsyncSession, **kwargs):
    query = select(Block.block_name).where((Block.is_visible == True) &
                                           (Block.date_to_post > datetime.datetime.now())).order_by(Block.date_to_post)
    result = await session.execute(query)
    return result.fetchall()


async def get_order_block(session: AsyncSession, **kwargs):
    query = select(Block).where(Block.is_visible == True).order_by(Block.date_to_post)
    result = await session.execute(query)
    return result.fetchall()


async def set_progres_block(session: AsyncSession, **kwargs):
    query = update(Block).where((Block.is_visible == True) & (Block.id == kwargs.get("block_id"))).values(
        progress_block=kwargs.get("progress"))
    await session.execute(query)
    await session.commit()


async def update_count_send_block_session_pool(session_pool, **kwargs):
    query = update(Block).where((Block.is_visible == True) & (Block.id == kwargs.get("block_id"))).values(
        count_send=Block.count_send + 1
    )
    async with session_pool.begin().async_session as session:
        await session.execute(query)
        await session.commit()


async def update_count_send_block_session(session, **kwargs):
    query = update(Block).where((Block.is_visible == True) & (Block.id == kwargs.get("block_id"))).values(
        count_send=Block.count_send + 1
    )
    await session.execute(query)
    await session.commit()


async def get_time_next_block(session: AsyncSession, **kwargs):
    query = select(Block.date_to_post).where(Block.progress_block == kwargs.get("progress_block"))
    result = await session.execute(query)
    return result.fetchone()


async def get_next_block_progress(session: AsyncSession, **kwargs):
    query = select(Block.progress_block).where \
        (Block.date_to_post >= datetime.datetime.now()).order_by(Block.date_to_post).limit(1)
    result = await session.execute(query)
    return result.fetchone()


async def get_date_post_block_by_name(session: AsyncSession, **kwargs):
    query = select(Block.date_to_post).where(Block.block_name == kwargs.get("block_name"))
    result = await session.execute(query)
    return result.fetchone()


async def set_date_post_block_by_name(session: AsyncSession, **kwargs):
    query = update(Block).where((Block.is_visible == True) & (Block.block_name == kwargs.get("block_name"))).values(
        date_to_post=kwargs.get("date_to_post"))
    await session.execute(query)
    await session.commit()


async def delete_block(session: AsyncSession, **kwargs):
    query = update(Block).where((Block.is_visible == True) & (Block.id == kwargs.get("block_id"))).values(
        is_visible=False)
    await session.execute(query)
    await session.commit()


async def get_block_by_block_name(session: AsyncSession, **kwargs):
    query = select(Block).where(Block.block_name == kwargs.get("block_name"))
    result = await session.execute(query)
    return result.fetchone()


async def get_block_id_by_progress(session: AsyncSession, **kwargs):
    query = select(Block.id).where(Block.progress_block == kwargs.get("progress_block"))
    result = await session.execute(query)
    return result.fetchone()


async def get_block_progress_by_id(session: AsyncSession, **kwargs):
    query = select(Block.progress_block).where(Block.id == kwargs.get("block_id"))
    result = await session.execute(query)
    return result.fetchone()


async def get_order_block_progress(session_pool, **kwargs):
    query = select(Block.progress_block).where(Block.is_visible == True).order_by(Block.date_to_post)
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()

async def get_order_block_progress_session(session):
    query = select(Block.progress_block).where(Block.is_visible == True).order_by(Block.date_to_post)
    result = await session.execute(query)
    return result.fetchall()