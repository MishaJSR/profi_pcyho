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
    query = select(Users.user_id, Users.progress)
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()