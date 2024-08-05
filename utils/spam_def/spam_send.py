import asyncio
import datetime
import logging

from aiogram.types import InputMediaPhoto, ReplyKeyboardRemove

from database.orm_block.orm_query_block import get_block_session_pool_by_id, get_block_all_session_pool, \
    update_count_send_block_session_pool, get_order_block_progress
from database.orm_block.orm_query_block_pool import get_block_pool_all_session_pool
from database.orm_block.orm_query_block_pool_media import get_photos_id_from_block_pool_session_pool, \
    get_videos_id_from_block_pool_session_pool
from database.orm_block.orm_query_block_media import get_videos_id_from_block_session_pool, get_photos_id_from_block_session_pool
from database.orm_task.orm_query_task import get_tasks_by_block_id_session_pool
from database.orm_user.orm_query_user import get_all_users, update_last_send_block_session_pool, \
    update_users_progress_session_pool, get_user_info_for_mom, check_new_user_session_pool, \
    update_stop_spam, get_user_class_session_pool, get_all_users_updated, update_datetime, get_parent_by_id, \
    get_parent_by_session
from keyboards.admin.inline_admin import get_inline, get_inline_pay_end, get_inline_parent_all_block_pay, \
    get_inline_teacher_all_block_referal
from keyboards.user.reply_user import start_kb
from utils.common.message_constant import you_should_be_partner, ready_to_task, text_for_media, file_id, \
    congratulations, question_answer, remind_message, message_third_block


async def send_progress_mom(bot, session_pool):
    await asyncio.sleep(5)
    while True:
        try:
            data = await get_user_info_for_mom(session_pool)
            blocks = await get_order_block_progress(session_pool)
            max_progress = blocks[-1][0]
            for child in data:
                parent_id, progress, points = child
                try:
                    res = await check_new_user_session_pool(session_pool, user_id=parent_id)

                    mom_id, stop_spam = res[0], res[1]
                    if stop_spam:
                        return
                    if progress == (max_progress + 1):
                        await bot.send_message(chat_id=mom_id,
                                               text=f"Поздравляю!!! Ваш ребенок прошел весь курс\n"
                                                    f"На этом его бесплатное обучение завершено\n"
                                                    f"Вы можете попробовать для ребёнка наш полный курс",
                                               reply_markup=get_inline_pay_end())
                        await update_stop_spam(session_pool, user_id=mom_id)
                    elif progress < 2:
                        await bot.send_message(chat_id=mom_id,
                                               text=f"Ваш ребенок пока еще не проходил уроки\n"
                                                    f"Но мы верим что у него все получится " + "🥰")
                    elif points == 0 and progress > 1:
                        await bot.send_message(chat_id=mom_id,
                                               text=f"Ваш ребенок большой молодец и уже прошёл {progress - 1} блоков\n"
                                                    f"Мы верим что у него все получится " + "🥰")
                    else:
                        await bot.send_message(chat_id=mom_id,
                                               text=f"Ваш ребёнок делает большие успехи!!!\n"
                                                    f"Он заработал {points} очков и уже прошёл {progress - 1} блоков\n"
                                                    f"Мы верим что у него все получится " + "🥰")
                except Exception as e:
                    logging.info(e)
        except Exception as e:
            pass
        finally:
            await asyncio.sleep(216000)


async def send_remind(bot, session_pool):
    await asyncio.sleep(5)
    while True:
        try:
            users = await get_all_users_updated(session_pool)
            for user in users:
                user_data = user._data
                seconds = (datetime.datetime.now() - user_data[1]).total_seconds()
                if seconds > 216000 and user_data[2] < 3:
                    await bot.send_message(chat_id=user_data[0], text=remind_message)
                    await update_datetime(session_pool, user_id=user_data[0])
        except Exception as e:
            pass
        finally:
            await asyncio.sleep(3600)


async def spam_task(bot, session_pool, engine):
    await asyncio.sleep(5)

    while True:
        try:
            now_time = datetime.datetime.now()
            block_to_send = {}
            users = await get_all_users(session_pool)
            active_blocks = await get_block_all_session_pool(session_pool)
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
                    await send_spam(bot, session_pool, user[0], block_id_to_send)
                    await update_last_send_block_session_pool(session_pool, user_id=user[0], block_id=block_id_to_send)
        except Exception as e:
            logging.info(e)
        await asyncio.sleep(10)


async def send_spam(bot, session_pool, user_id, block_id):
    try:
        block = await get_block_session_pool_by_id(session_pool, block_id=block_id)
        if not block:
            # await send_vebinar(bot, session_pool, user_id, block_id)
            return
        tasks = await get_tasks_by_block_id_session_pool(session_pool, block_id=block_id)
        has_tasks = True
        if len(tasks) == 0:
            has_tasks = False
        content = block._data[0].content
        callback = block._data[0].callback_button_id
        block_id = block._data[0].id
        if block._data[0].is_sub_block:
            await send_multi_post(bot, session_pool, user_id=user_id, block_id=block_id, has_tasks=has_tasks,
                                  callback=callback)
            return
        if not block._data[0].has_media:
            await bot.send_message(chat_id=user_id, text=content)
            if has_tasks:
                if block._data[0].progress_block == 1:
                    await bot.send_message(chat_id=user_id, text=ready_to_task,
                                           reply_markup=get_inline(callback_data=callback))
                if block._data[0].progress_block == 2:
                    await bot.send_message(chat_id=user_id, text='Реши кейсы с нашими ребятами! У тебя все получится💯',
                                           reply_markup=get_inline(is_second=True, callback_data=callback))

            else:
                await no_task_end_script(bot, session_pool, user_id)
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
                await bot.send_video(user_id, video=video_id)
        await update_count_send_block_session_pool(session_pool, block_id=block_id)
        if has_tasks:
            if block._data[0].progress_block == 1:
                await bot.send_message(chat_id=user_id, text=ready_to_task,
                                       reply_markup=get_inline(callback_data=callback))
            if block._data[0].progress_block == 2:
                await bot.send_message(chat_id=user_id, text='Реши кейсы с нашими ребятами! У тебя все получится💯',
                                       reply_markup=get_inline(is_second=True, callback_data=callback))
        else:
            await no_task_end_script(bot, session_pool, user_id)

    except Exception as e:
        await bot.send_message(chat_id=548349299, text=f'Ошибка при попытке подключения к базе данных {e}',
                               reply_markup=start_kb())
        return


async def send_multi_post(bot, session_pool, user_id, block_id, has_tasks, callback):
    block_pool = await get_block_pool_all_session_pool(session_pool, block_main_id=block_id)
    for block in block_pool:
        content = block._data[0].content
        has_media = block._data[0].has_media
        block_pool_id = block._data[0].id
        if not has_media:
            await bot.send_message(chat_id=user_id, text=content)
        else:
            media_group = []
            photo_ids = await get_photos_id_from_block_pool_session_pool(session_pool, block_pool_id=block_pool_id)
            videos_ids = await get_videos_id_from_block_pool_session_pool(session_pool, block_pool_id=block_pool_id)
            video_content = [video._data[0] for video in videos_ids]
            photo_content = [photo._data[0] for photo in photo_ids]
            if photo_ids:
                for index, photo_id in enumerate(photo_content):
                    if index == 0:
                        media_group.append(InputMediaPhoto(type='photo', media=photo_id, caption=content))
                    else:
                        media_group.append(InputMediaPhoto(type='photo', media=photo_id))
            if media_group:
                await bot.send_media_group(user_id, media=media_group)
            else:
                await bot.send_message(chat_id=user_id, text=content)
            if videos_ids:
                for video_id in video_content:
                    await bot.send_video(user_id, video=video_id)

    if not has_tasks:
        await no_task_end_script(bot, session_pool, user_id)
        return
    await bot.send_message(chat_id=user_id, text=ready_to_task,
                           reply_markup=get_inline(callback_data=callback))
    await update_count_send_block_session_pool(session_pool, block_id=block_id)


async def no_task_end_script(bot, session_pool, user_id):
    user_class = await get_user_class_session_pool(session_pool, user_id=user_id)
    if user_class[0] == "Ребёнок":
        await bot.send_message(chat_id=user_id,
                               text=congratulations,
                               reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=user_id, text=question_answer)
        parents = await get_parent_by_session(session_pool, user_id=user_id)
        for parent in parents:
            mom_id = parent[0]
            try:
                await bot.send_message(chat_id=mom_id,
                                       text=message_third_block,
                                       reply_markup=get_inline_pay_end())
            except Exception as e:
                pass
    elif user_class[0] == "Родитель":
        await bot.send_message(chat_id=user_id,
                               text=f"Поздравляю!\n"
                                    f"Первая глава квеста завершена🔥\n"
                                    f"Вы также можете оплатить полный курс по ссылке",
                               reply_markup=get_inline_parent_all_block_pay())
        await bot.send_message(chat_id=user_id, text=question_answer)
    else:
        await bot.send_message(chat_id=user_id,
                               text=f"Поздравляю!\n"
                                    f"Первая глава квеста завершена🔥\n"
                                    f"{you_should_be_partner}",
                               reply_markup=get_inline_teacher_all_block_referal())
        await bot.send_message(chat_id=user_id, text=question_answer)
    await update_users_progress_session_pool(session_pool, user_id=user_id)
