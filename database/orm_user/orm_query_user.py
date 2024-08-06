import datetime

from database.models import Users, UsersTaskProgress
from sqlalchemy import select, update, delete


async def check_new_user(session, user_id):
    query = select(Users.user_id).where(Users.user_id == user_id)
    result = await session.execute(query)
    return result.fetchone()


async def check_new_user_session_pool(session_pool, user_id):
    query = select(Users.user_id, Users.stop_spam).where((Users.user_id == user_id) and (Users.user_block_bot == False))
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchone()


async def check_new_user_session(session, user_id):
    query = select(Users.user_id).where((Users.user_id == user_id) and (Users.user_block_bot == False))
    result = await session.execute(query)
    return result.fetchone()


async def add_user(session, user_id: int, username: str, user_tag: str, user_class: str, is_subscribe=False,
                   parent_id=None,
                   progress=0):
    if not user_tag:
        user_tag = '@'
    else:
        user_tag = '@' + user_tag
    obj = Users(
        user_id=user_id,
        username=username,
        user_class=user_class,
        user_tag=user_tag,
        parent_id=parent_id,
        is_subscribe=is_subscribe,
        progress=progress
    )
    session.add(obj)
    await session.commit()


async def get_all_users_id(session, **kwargs):
    query = select(Users.user_id)
    result = await session.execute(query)
    return result.fetchall()


async def get_all_users_id_progress(session, **kwargs):
    query = select(Users.user_id, Users.progress).where(Users.user_block_bot == False)
    result = await session.execute(query)
    return result.fetchall()


async def get_all_users(session_pool, **kwargs):
    query = select(Users.user_id, Users.progress,
                   Users.id_last_block_send, Users.user_class,
                   Users.user_become_children).where((Users.is_subscribe == True) and (Users.user_block_bot == False))
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()

async def get_all_users_session(session, **kwargs):
    query = select(Users.user_id, Users.progress,
                   Users.id_last_block_send, Users.user_class,
                   Users.user_become_children, Users.is_subscribe).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchall()


async def get_all_users_updated(session_pool, **kwargs):
    query = select(Users.user_id, Users.updated, Users.progress).where((Users.user_block_bot == False))
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()


async def get_progress_by_user_id(session, **kwargs):
    query = select(Users.progress).where((Users.user_id == kwargs.get("user_id") and (Users.user_block_bot == False)))
    result = await session.execute(query)
    return result.fetchone()


async def update_user_progress(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        progress=Users.progress + 1)
    await session.execute(query)
    await session.commit()


async def update_user_become(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        user_become_children=True)
    await session.execute(query)
    await session.commit()


async def update_user_phone(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        phone_number=kwargs.get("phone_number"), is_subscribe=True)
    await session.execute(query)
    await session.commit()


async def update_user_subscribe(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        is_subscribe=True)
    await session.execute(query)
    await session.commit()


async def update_users_progress_session_pool(session_pool, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        progress=Users.progress + 1)
    async with session_pool.begin().async_session as session:
        await session.execute(query)
        await session.commit()


async def update_users_progress_session(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        progress=Users.progress + 1)
    await session.execute(query)
    await session.commit()


async def update_datetime(session_pool, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        updated=datetime.datetime.now())
    async with session_pool.begin().async_session as session:
        await session.execute(query)
        await session.commit()


async def update_user_block_bot_session_pool(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(user_block_bot=True)
    await session.execute(query)
    await session.commit()


async def update_user_points(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        points=Users.points + kwargs.get("points"))
    await session.execute(query)
    await session.commit()


async def update_parent_id(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        parent_id=kwargs.get("parent_id"), is_subscribe=True)
    await session.execute(query)
    await session.commit()


async def update_user_callback(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        user_callback=kwargs.get("user_callback"))
    await session.execute(query)
    await session.commit()


async def get_user_points(session, **kwargs):
    query = select(Users.points).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchone()


async def get_user_parent(session, **kwargs):
    query = select(Users.parent_id).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchone()


async def get_user_class(session, **kwargs):
    query = select(Users.user_class, Users.user_become_children).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchone()


async def check_user_subscribe(session, **kwargs):
    query = select(Users.is_subscribe, Users.progress, Users.user_class, Users.user_callback,
                   Users.user_become_children,
                   Users.name_of_user).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchone()


async def check_user_become_children(session, **kwargs):
    query = select(Users.user_become_children).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchone()


async def check_user_subscribe_new_user(session, **kwargs):
    query = select(Users.is_subscribe, Users.user_class, Users.user_callback, Users.phone_number,
                   Users.name_of_user).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchone()


async def get_user_info_for_mom(session_pool, **kwargs):
    query = select(Users.parent_id, Users.progress, Users.points).where(
        (Users.user_class == "Ребёнок") and (Users.is_subscribe == True))
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()


async def get_parent_by_id(session, user_id):
    query = select(Users.parent_id, Users.progress, Users.points).where(
        (Users.user_id == user_id) and (Users.is_subscribe == True))
    result = await session.execute(query)
    return result.fetchall()


async def get_parent_by_session(session_pool, user_id):
    query = select(Users.parent_id, Users.progress, Users.points).where(
        (Users.user_id == user_id) and (Users.is_subscribe == True))
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchall()


async def get_parent_by_ses(session, user_id):
    query = select(Users.parent_id, Users.progress, Users.points).where(
        (Users.user_id == user_id) and (Users.is_subscribe == True))
    result = await session.execute(query)
    return result.fetchall()


async def get_user_class_session_pool(session_pool, **kwargs):
    query = select(Users.user_class).where(Users.user_id == kwargs.get("user_id"))
    async with session_pool.begin().async_session as session:
        result = await session.execute(query)
    return result.fetchone()


async def get_user_class_session(session, **kwargs):
    query = select(Users.user_class).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchone()


async def update_last_send_block_session_pool(session_pool, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        id_last_block_send=kwargs.get("block_id"))
    async with session_pool.begin().async_session as session:
        await session.execute(query)
        await session.commit()

async def update_last_send_block_session(session, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        id_last_block_send=kwargs.get("block_id"))
    await session.execute(query)
    await session.commit()


async def update_stop_spam(session_pool, **kwargs):
    query = update(Users).where(Users.user_id == kwargs.get("user_id")).values(
        stop_spam=True)
    async with session_pool.begin().async_session as session:
        await session.execute(query)
        await session.commit()


async def get_users_for_excel_all(session, **kwargs):
    query = select(Users.user_id, Users.username, Users.user_tag, Users.user_class, Users.phone_number,
                   Users.is_subscribe, Users.parent_id,
                   Users.user_become_children, Users.user_callback,
                   Users.points)
    result = await session.execute(query)
    return result.all()


async def get_users_for_excel_parents(session, **kwargs):
    query = select(Users.user_id, Users.username, Users.user_tag, Users.user_class, Users.phone_number,
                   Users.is_subscribe, Users.parent_id,
                   Users.user_become_children, Users.user_callback,
                   Users.points).where(Users.user_class == "Родитель")
    result = await session.execute(query)
    return result.all()


async def get_users_for_excel_teacher(session, **kwargs):
    query = select(Users.user_id, Users.username, Users.user_tag, Users.user_class, Users.phone_number,
                   Users.is_subscribe, Users.parent_id,
                   Users.user_become_children, Users.user_callback,
                   Users.points).where(Users.user_class == "Педагог")
    result = await session.execute(query)
    return result.all()


async def delete_me_user(session, **kwargs):
    query1 = delete(Users).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query1)
    await session.commit()


async def get_user_progress(session, **kwargs):
    query = select(Users.progress, Users.points).where(Users.user_id == kwargs.get("user_id"))
    result = await session.execute(query)
    return result.fetchone()


async def get_user_points(session, **kwargs):
    query = select(Users.points).where(Users.user_id == kwargs.get("user_id")).where(Users.points > 0)
    result = await session.execute(query)
    return result.fetchone()
