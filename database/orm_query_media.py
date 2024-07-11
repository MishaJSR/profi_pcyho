import calendar
import datetime
import logging
import sqlite3

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task, Users, Media
from sqlalchemy import select, delete, update
import pandas as pd
import re


async def add_media(session: AsyncSession, **kwargs):
    obj = Media(
        block_id=kwargs.get("block_id"),
        photo_id=kwargs.get("photo_id"),
        video_id=kwargs.get("video_id"),
        callback_button_id=kwargs.get("callback_button_id"),
    )
    session.add(obj)
    await session.commit()