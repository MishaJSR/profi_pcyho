import calendar
import datetime
import logging
import sqlite3

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task, Users, MediaBlock
from sqlalchemy import select, delete, update
import pandas as pd
import re


async def get_task_by_block_id(session: AsyncSession, **kwargs):
    pass
    query = select(Task).where((Task.is_visible == True) & (Task.block_id == kwargs.get('block_id')))
    result = await session.execute(query)
    return result.fetchall()

async def get_task_for_delete(session: AsyncSession, **kwargs):
    pass
    query = select(Task).where((Task.is_visible == True) & (Task.block_id == kwargs.get('task_id')))
    result = await session.execute(query)
    return result.fetchall()


async def add_task_image(session: AsyncSession, **kwargs):
    obj = Task(
        block_id=kwargs.get("block_id"),
        description=kwargs.get("description"),
        answer_mode=kwargs.get("answer_mode"),
        answer=kwargs.get("answer"),
    )
    session.add(obj)
    await session.commit()


async def add_task_test(session: AsyncSession, **kwargs):
    obj = Task(
        block_id=kwargs.get("block_id"),
        description=kwargs.get("description"),
        answer_mode=kwargs.get("answer_mode"),
        answers=kwargs.get("answers"),
        answer=kwargs.get("answer"),
    )
    session.add(obj)
    await session.commit()


async def delete_task(session: AsyncSession, **kwargs):
    query = update(Task).where((Task.is_visible == True) & (Task.id == kwargs.get("task_id"))).values(is_visible=False)
    await session.execute(query)
    await session.commit()
