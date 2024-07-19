from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task
from sqlalchemy import select, update


async def get_task_by_block_id(session: AsyncSession, **kwargs):
    pass
    query = select(Task).where((Task.is_visible == True) & (Task.block_id == kwargs.get('block_id')))
    result = await session.execute(query)
    return result.fetchall()


async def get_tasks_by_block_id_session_pool(session_pool, **kwargs):
    query = select(Task).where((Task.is_visible == True) & (Task.block_id == kwargs.get('block_id')))
    async with session_pool.begin().async_session as session:
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
    return obj.id


async def add_task_test(session: AsyncSession, **kwargs):
    obj = Task(
        block_id=kwargs.get("block_id"),
        description=kwargs.get("description"),
        answer_mode=kwargs.get("answer_mode"),
        answers=kwargs.get("answers"),
        answer=kwargs.get("answer"),
        addition=kwargs.get("addition")
    )
    session.add(obj)
    await session.commit()
    return obj.id


async def delete_task(session: AsyncSession, **kwargs):
    query = update(Task).where((Task.is_visible == True) & (Task.id == kwargs.get("task_id"))).values(is_visible=False)
    await session.execute(query)
    await session.commit()



