import calendar
import datetime
import logging
import sqlite3

from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task, Users, MediaBlock
from sqlalchemy import select, delete, update
import pandas as pd
import re


async def add_media(session: AsyncSession, **kwargs):
    obj = MediaBlock(
        block_id=kwargs.get("block_id"),
        photo_id=kwargs.get("photo_id"),
        video_id=kwargs.get("video_id"),
    )
    session.add(obj)
    await session.commit()


async def get_videos_id_from_block(session: AsyncSession, **kwargs):
    query = select(MediaBlock.video_id).where((MediaBlock.block_id == kwargs.get("block_id"))
                                     & (MediaBlock.video_id != None))
    result = await session.execute(query)
    return result.fetchall()

async def get_videos_id_from_block_session_pool(session_pool, **kwargs):
    query = select(MediaBlock.video_id).where((MediaBlock.block_id == kwargs.get("block_id"))
                                     & (MediaBlock.video_id != None))
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()


async def get_photos_id_from_block(session: AsyncSession, **kwargs):
    query = select(MediaBlock.photo_id).where((MediaBlock.block_id == kwargs.get("block_id"))
                                     & (MediaBlock.photo_id != None))
    result = await session.execute(query)
    return result.fetchall()

async def get_photos_id_from_block_session_pool(session_pool, **kwargs):
    query = select(MediaBlock.photo_id).where((MediaBlock.block_id == kwargs.get("block_id"))
                                     & (MediaBlock.photo_id != None))
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()
