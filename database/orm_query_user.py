from database.models import Users
from sqlalchemy import select, update

async def check_new_user(session, user_id: int):
    query = select(Users.user_id).where(Users.user_id == user_id)
    result = await session.execute(query)
    return result.all()


async def add_user(session, user_id: int, username: str):
    if not username:
        username = ')'
    obj = Users(
        user_id=user_id,
        username=username
    )
    session.add(obj)
    await session.commit()



async def get_all_users_id(session, **kwargs):
    query = select(Users.user_id)
    result = await session.execute(query)
    return result.fetchall()

async def get_all_users_id_progress(session, **kwargs):
    query = select(Users.user_id, Users.progress)
    result = await session.execute(query)
    return result.fetchall()

async def get_all_users(session_pool, **kwargs):
    query = select(Users.user_id, Users.progress, Users.id_last_block_send)
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()


async def get_progress_by_user_id(session, **kwargs):
    query = select(Users.progress).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchone()


async def update_user_progress(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        progress=Users.progress + 1)
    await session.execute(query)
    await session.commit()


async def update_user_points(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        points=Users.points + kwargs.get("points"))
    await session.execute(query)
    await session.commit()

async def get_user_points(session, **kwargs):
    query = select(Users.points).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchone()


async def update_last_send_block_session_pool(session_pool, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        id_last_block_send=kwargs.get("block_id"))
    async with session_pool.begin().async_session as session:
        await session.execute(query)
        await session.commit()
