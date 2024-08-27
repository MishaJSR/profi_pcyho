import asyncio
import datetime
import logging
import os

from aiogram.types import InputMediaPhoto, FSInputFile

from database.orm_block.orm_query_block import get_block_all_session, get_block_session_by_id, \
    update_count_send_block_session
from database.orm_block.orm_query_block_pool import get_block_pool_all
from database.orm_block.orm_query_block_pool_media import get_photos_id_from_block_pool, get_videos_id_from_block_pool
from database.orm_block.orm_query_block_media import get_videos_id_from_block, get_photos_id_from_block
from database.orm_task.orm_query_task import get_task_by_block_id
from database.orm_user.orm_query_user import get_all_users_updated, update_datetime, get_all_users_session, \
    update_last_send_block_session, get_users_for_excel_all_session
from handlers.admin.admin_excel_loader_router import inplace_df
from keyboards.admin.inline_admin import get_inline, get_third_block1
from keyboards.user.reply_user import start_kb
from utils.common.message_constant import ready_to_task, remind_message


async def send_remind(bot, session_pool):
    logging.info("I start")
    await asyncio.sleep(5)
    a = [6, 24, 25, 26, 27, 28, 39, 40, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
         71, 72, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153]
    while True:
        logging.info("I circle")
        for el in a:
            try:
                await bot.forward_message(chat_id=-1002164443199, from_chat_id=-1002164443199, message_id=el)
                await asyncio.sleep(3)
            except Exception as e:
                logging.info(f"Image Exception {e}")
        logging.info("I wait")
        await asyncio.sleep(20000)


async def spam_task_user(bot, session, user_id):
    try:
        now_time = datetime.datetime.now()
        block_to_send = {}
        users = await get_all_users_session(session, user_id=user_id)
        if not users[0]._data[5]:
            return
        active_blocks = await get_block_all_session(session)
        for block in active_blocks:
            if block._data[0].date_to_post <= now_time:
                block_to_send[block._data[0].progress_block] = block._data[0].id
        for user in users:
            if user[1] == 2 and user[3] != "Ребёнок" and not (user[4]):
                continue
            block_id_to_send = block_to_send.get(user[1])
            if not block_id_to_send:
                continue
            if block_id_to_send != user[2] or user[2] == 0:
                await send_spam_user(bot, session, user[0], block_id_to_send)
                await update_last_send_block_session(session, user_id=user[0], block_id=block_id_to_send)
    except Exception as e:
        logging.info(e)


async def send_spam_user(bot, session, user_id, block_id):
    try:
        block = await get_block_session_by_id(session, block_id=block_id)
        if not block:
            return
        tasks = await get_task_by_block_id(session, block_id=block_id)
        has_tasks = True
        if len(tasks) == 0:
            has_tasks = False
        content = block._data[0].content
        callback = block._data[0].callback_button_id
        block_id = block._data[0].id
        if block._data[0].is_sub_block:
            await send_multi_post_user(bot, session, user_id=user_id, block_id=block_id, has_tasks=has_tasks,
                                       callback=callback, progress=block._data[0].progress_block)
            return
        if not block._data[0].has_media:
            await bot.send_message(chat_id=user_id, text=content)
            if has_tasks:
                if block._data[0].progress_block == 1:
                    await bot.send_message(chat_id=user_id, text=ready_to_task,
                                           reply_markup=get_inline(callback_data=callback))
                if block._data[0].progress_block == 2:
                    await bot.send_message(chat_id=user_id, text='Готов к практическому заданию?',
                                           reply_markup=get_inline(is_second=True, callback_data=callback))

            else:
                await no_task_end_script_user(bot, user_id)
            return
        video_content = await get_videos_id_from_block(session, block_id=block_id)
        photo_content = await get_photos_id_from_block(session, block_id=block_id)
        video_content = [video._data[0] for video in video_content]
        photo_content = [photo._data[0] for photo in photo_content]
        media_group = []
        for index, photo_id in enumerate(photo_content):
            if index == 0:
                media_group.append(InputMediaPhoto(type='photo', media=photo_id, caption=content))
            else:
                media_group.append(InputMediaPhoto(type='photo', media=photo_id))
        if media_group:
            await bot.send_media_group(user_id, media=media_group)
        if video_content:
            for index, video_id in enumerate(video_content):
                await bot.send_video(user_id, video=video_id)
        await update_count_send_block_session(session, block_id=block_id)
        if has_tasks:
            if block._data[0].progress_block == 1:
                await bot.send_message(chat_id=user_id, text=ready_to_task,
                                       reply_markup=get_inline(callback_data=callback))
            if block._data[0].progress_block == 2:
                await bot.send_message(chat_id=user_id, text='Реши кейсы с нашими ребятами! У тебя все получится💯',
                                       reply_markup=get_inline(is_second=True, callback_data=callback))
        else:
            await no_task_end_script_user(bot, user_id)

    except Exception as e:
        await bot.send_message(chat_id=548349299, text=f'Ошибка при попытке подключения к базе данных {e}',
                               reply_markup=start_kb())
        return


async def send_multi_post_user(bot, session, user_id, block_id, has_tasks, callback, progress):
    block_pool = await get_block_pool_all(session, block_main_id=block_id)
    for block in block_pool:
        content = block._data[0].content
        if content == "**":
            content = None

        has_media = block._data[0].has_media
        block_pool_id = block._data[0].id
        if not has_media:
            await bot.send_message(chat_id=user_id, text=content)
        else:
            media_group = []
            photo_ids = await get_photos_id_from_block_pool(session, block_pool_id=block_pool_id)
            videos_ids = await get_videos_id_from_block_pool(session, block_pool_id=block_pool_id)
            video_content = [video._data[0] for video in videos_ids]
            photo_content = [photo._data[0] for photo in photo_ids]
            if photo_ids:
                for index, photo_id in enumerate(photo_content):
                    if index == 0 and content:
                        media_group.append(InputMediaPhoto(type='photo', media=photo_id, caption=content))
                    else:
                        media_group.append(InputMediaPhoto(type='photo', media=photo_id))
            if media_group:
                await bot.send_media_group(user_id, media=media_group)
                await asyncio.sleep(5)
            else:
                await bot.send_message(chat_id=user_id, text=content)
            if videos_ids:
                for video_id in video_content:
                    await bot.send_video(user_id, video=video_id)

    if not has_tasks:
        await no_task_end_script_user(bot, user_id)
        return
    if progress == 2:
        await bot.send_message(chat_id=user_id, text="Реши кейсы с нашими ребятами! У тебя все получится💯",
                               reply_markup=get_inline(callback_data=callback))
    await update_count_send_block_session(session, block_id=block_id)


async def no_task_end_script_user(bot, user_id):
    await bot.send_message(chat_id=user_id, text="Пункт об увлечениях заполнен?", reply_markup=get_third_block1())
