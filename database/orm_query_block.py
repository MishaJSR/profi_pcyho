import calendar
import datetime
import logging
import sqlite3

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task, Users, Block
from sqlalchemy import select, delete, update
import pandas as pd
import re


async def add_block(session: AsyncSession, **kwargs):
    obj = Block(
        block_name=kwargs.get("block_name"),
        content=kwargs.get("content"),
        has_media=kwargs.get("has_media"),
        date_to_post=kwargs.get("date_to_post"),
        progress_block=kwargs.get("progress_block"),
        callback_button_id=kwargs.get("callback_button_id"),
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj.id


async def get_block_for_add_task(session: AsyncSession, **kwargs):
    query = select(Block).where((Block.is_visible == True) & (Block.is_vebinar == False))
    result = await session.execute(query)
    return result.fetchall()


async def get_block_active(session: AsyncSession, **kwargs):
    query = select(Block).where((Block.is_visible == True) & (Block.is_vebinar == False))
    result = await session.execute(query)
    return result.fetchall()


async def get_block_by_id(session: AsyncSession, **kwargs):
    query = select(Block).where((Block.is_visible == True) & (Block.is_vebinar == False) & (Block.id == kwargs.get("block_id")))
    result = await session.execute(query)
    return result.fetchone()


async def delete_block(session: AsyncSession, **kwargs):
    query = update(Block).where((Block.is_visible == True) & (Block.id == kwargs.get("block_id"))).values(
        is_visible=False)
    await session.execute(query)
    await session.commit()
