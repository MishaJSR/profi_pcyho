import calendar
import datetime
import logging
import sqlite3

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task, Users, MediaVideo
from sqlalchemy import select, delete, update
import pandas as pd
import re


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

