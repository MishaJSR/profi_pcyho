import logging
import os
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats, InputMediaPhoto
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from dotenv import find_dotenv, load_dotenv
import betterlogging as bl

from database.config import load_config
from database.orm_query_block import get_block_by_id, get_block_all_session_pool, get_block_session_pool_by_id
from database.orm_query_media_block import get_videos_id_from_block, get_photos_id_from_block, \
    get_videos_id_from_block_session_pool, get_photos_id_from_block_session_pool
from database.orm_query_user import get_all_users, update_last_send_block_session_pool
from keyboards.admin.inline_admin import get_inline
from keyboards.admin.reply_admin import start_kb

import datetime

load_dotenv(find_dotenv())

from handlers.user.user_main_router import user_private_router
from handlers.admin.admin_main_router import admin_private_router
from common.bot_cmd_list import private
from middlewares.db import DataBaseSession
from database.engine import create_engine, create_session_pool


def get_storage(config):
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()

def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")






async def on_startup(bot):
    print('Bot start')


async def on_shutdown(bot):
    print('Bot end')


async def main():
    print('start')

    setup_logging()
    config = load_config()
    storage = get_storage(config)

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)
    dp.include_routers(admin_private_router, user_private_router)

    engine = create_engine(config.db)
    session_pool = create_session_pool(engine)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_pool))

    task = asyncio.create_task(my_task(bot, session_pool))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)



async def my_task(bot, session_pool):
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
                    return
                if block_id_to_send != user[2] or user[2] == 0:
                    await send_spam(bot, session_pool, user[0], block_id_to_send)
                    await update_last_send_block_session_pool(session_pool, user_id=user[0], block_id=block_id_to_send)


        except Exception as e:
            print('error', e)
        # await send_spam(bot, session_pool)
        await asyncio.sleep(20)  # 300 seconds = 5 minutes


async def send_spam(bot, session_pool, user_id, block_id):
    try:
        block = await get_block_session_pool_by_id(session_pool, block_id=block_id)
        content = block._data[0].content
        callback = block._data[0].callback_button_id
        block_id = block._data[0].id

        if not block._data[0].has_media:
            await bot.send_message(chat_id=user_id, text=content, reply_markup=get_inline(callback_data=callback))
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

        else:
            await bot.send_message(chat_id=user_id, text="Пройти тест по блоку")

    except Exception as e:
        await bot.send_message(chat_id=user_id, text=f'Ошибка при попытке подключения к базе данных {e}', reply_markup=start_kb())
        return

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот был выключен!")
