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
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj.id