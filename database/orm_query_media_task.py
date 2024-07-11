import calendar
import datetime
import logging
import sqlite3

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task, Users, MediaVideo, MediaTask
from sqlalchemy import select, delete, update
import pandas as pd
import re


async def add_media_task(session: AsyncSession, **kwargs):
    obj = MediaTask(
        task_id=kwargs.get("task_id"),
        photo_id=kwargs.get("photo_id")
    )
    session.add(obj)
    await session.commit()


