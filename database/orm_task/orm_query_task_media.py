from sqlalchemy.ext.asyncio import AsyncSession
from database.models import MediaTask
from sqlalchemy import select



async def add_media_task(session: AsyncSession, **kwargs):
    obj = MediaTask(
        task_id=kwargs.get("task_id"),
        photo_id=kwargs.get("photo_id")
    )
    session.add(obj)
    await session.commit()


async def get_media_task_by_task_id(session: AsyncSession, **kwargs):
    query = select(MediaTask.photo_id).where((MediaTask.task_id == kwargs.get("task_id")))
    result = await session.execute(query)
    return result.fetchall()


