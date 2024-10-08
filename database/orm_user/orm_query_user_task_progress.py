from sqlalchemy.ext.asyncio import AsyncSession
from database.models import UsersTaskProgress
from sqlalchemy import select, delete


async def set_user_task_progress(session, **kwargs):
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


async def get_task_progress_by_user_id(session: AsyncSession, **kwargs):
    query = select(UsersTaskProgress).where((UsersTaskProgress.user_id == kwargs.get('user_id')) &
                                            (UsersTaskProgress.block_id == kwargs.get('block_id')))
    result = await session.execute(query)
    return result.fetchall()


async def get_is_pass_by_id(session: AsyncSession, block_id, user_id):
    query = select(UsersTaskProgress.is_pass).where((UsersTaskProgress.user_id == user_id) &
                                            (UsersTaskProgress.block_id == block_id))
    result = await session.execute(query)
    return result.fetchall()


async def delete_all_user_progress(session, **kwargs):
    query = delete(UsersTaskProgress).where(UsersTaskProgress.user_id == kwargs.get("user_id"))
    await session.execute(query)
    await session.commit()
