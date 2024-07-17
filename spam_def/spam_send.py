import asyncio
import datetime

from aiogram.types import InputMediaPhoto

from database.orm_query_block import get_block_session_pool_by_id, get_block_all_session_pool, \
    update_count_send_block_session_pool, get_block_vebinar_session_pool_by_id
from database.orm_query_media_block import get_videos_id_from_block_session_pool, get_photos_id_from_block_session_pool
from database.orm_query_user import get_all_users, update_last_send_block_session_pool
from keyboards.admin.inline_admin import get_inline
from keyboards.user.reply_user import start_kb


async def spam_task(bot, session_pool):
    print('start')
    await asyncio.sleep(5)
    while True:
        print("Task is running...")
        try:
            now_time = datetime.datetime.now()
            block_to_send = {}
            users = await get_all_users(session_pool)
            active_blocks = await get_block_all_session_pool(session_pool)
            for block in active_blocks:
                if block._data[0].date_to_post <= now_time:
                    block_to_send[block._data[0].progress_block] = block._data[0].id
            for user in users:
                block_id_to_send = block_to_send.get(user[1])
                if not block_id_to_send:
                    continue
                if block_id_to_send != user[2] or user[2] == 0:
                    await send_spam(bot, session_pool, user[0], block_id_to_send)
                    await update_last_send_block_session_pool(session_pool, user_id=user[0], block_id=block_id_to_send)
        except Exception as e:
            print('error', e)
        await asyncio.sleep(20)


async def send_spam(bot, session_pool, user_id, block_id):
    try:
        block = await get_block_session_pool_by_id(session_pool, block_id=block_id)
        if not block:
            #await send_vebinar(bot, session_pool, user_id, block_id)
            return
        content = block._data[0].content
        callback = block._data[0].callback_button_id
        block_id = block._data[0].id

        if not block._data[0].has_media:
            await bot.send_message(chat_id=user_id, text=content, reply_markup=get_inline(callback_data=callback))
            await update_count_send_block_session_pool(session_pool, block_id=block_id)
            return
        video_content = await get_videos_id_from_block_session_pool(session_pool, block_id=block_id)
        photo_content = await get_photos_id_from_block_session_pool(session_pool, block_id=block_id)
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
                if index == len(video_content) - 1:
                    await bot.send_video(user_id, video=video_id, reply_markup=get_inline(callback_data=callback))
                else:
                    await bot.send_video(user_id, video=video_id)
            await update_count_send_block_session_pool(session_pool, block_id=block_id)
        else:
            await update_count_send_block_session_pool(session_pool, block_id=block_id)
            await bot.send_message(chat_id=user_id, text="Пройти тест по блоку", reply_markup=get_inline(callback_data=callback))

    except Exception as e:
        await bot.send_message(chat_id=548349299, text=f'Ошибка при попытке подключения к базе данных {e}', reply_markup=start_kb())
        return


# async def send_vebinar(bot, session_pool, user_id, block_id):
#     try:
#         block = await get_block_vebinar_session_pool_by_id(session_pool, block_id=block_id)
#         content = block._data[0].content
#         block_id = block._data[0].id
#         if not block._data[0].has_media:
#             await bot.send_message(chat_id=user_id, text=content)
#             await bot.send_message(chat_id=user_id, text="Перейти на вебинар", reply_markup=get_inline_veb())
#             await update_count_send_block_session_pool(session_pool, block_id=block_id)
#             return
#         video_content = await get_videos_id_from_block_session_pool(session_pool, block_id=block_id)
#         photo_content = await get_photos_id_from_block_session_pool(session_pool, block_id=block_id)
#         video_content = [video._data[0] for video in video_content]
#         photo_content = [photo._data[0] for photo in photo_content]
#         media_group = []
#         for index, photo_id in enumerate(photo_content):
#             if index == 0:
#                 media_group.append(InputMediaPhoto(type='photo', media=photo_id, caption=content))
#             else:
#                 media_group.append(InputMediaPhoto(type='photo', media=photo_id))
#         if media_group:
#             await bot.send_media_group(user_id, media=media_group)
#         if video_content:
#             for index, video_id in enumerate(video_content):
#                 if index == len(video_content) - 1:
#                     await bot.send_video(user_id, video=video_id)
#                 else:
#                     await bot.send_video(user_id, video=video_id)
#             await update_count_send_block_session_pool(session_pool, block_id=block_id)
#         else:
#             await update_count_send_block_session_pool(session_pool, block_id=block_id)
#             await bot.send_message(chat_id=user_id, text="Пройти тест по блоку")
#         await bot.send_message(chat_id=user_id, text="Перейти на вебинар", reply_markup=get_inline_veb())
#
#     except Exception as e:
#         await bot.send_message(chat_id=548349299, text=f'Ошибка при попытке подключения к базе данных {e}', reply_markup=start_kb())
#         return