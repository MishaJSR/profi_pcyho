import calendar
import datetime
import logging
import sqlite3

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task, Users, MediaBlock, UsersTaskProgress
from sqlalchemy import select, delete, update
import pandas as pd
import re

async def set_user_progress(session, **kwargs):
    obj = UsersTaskProgress(
        user_id=kwargs.get("user_id"),
        username=kwargs.get("username"),
        block_id=kwargs.get("block_id"),
        task_id=kwargs.get("task_id"),
        answer_mode=kwargs.get("answer_mode"),
        result=kwargs.get("result"),
        is_pass=kwargs.get("is_pass"),
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj.id


