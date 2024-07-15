import calendar
import datetime
import logging
import sqlite3

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task, Users, MediaBlock
from sqlalchemy import select, delete, update
import pandas as pd
import re


async def get_all_users(session_pool, **kwargs):
    query = select(Users.user_id, Users.progress, Users.id_last_block_send)
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()


async def get_progress_by_user_id(session, **kwargs):
    query = select(Users.progress).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchone()


async def update_user_progress(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        progress=Users.progress + 1)
    await session.execute(query)
    await session.commit()


async def update_user_points(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        points=Users.points + kwargs.get("points"))
    await session.execute(query)
    await session.commit()

async def get_user_points(session, **kwargs):
    query = select(Users.points).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchone()


async def update_last_send_block_session_pool(session_pool, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        id_last_block_send=kwargs.get("block_id"))
    async with session_pool.begin().async_session as session:
        await session.execute(query)
        await session.commit()
