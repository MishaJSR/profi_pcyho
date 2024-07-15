from aiogram.types import InputMediaPhoto

from database.orm_query_block import get_block_session_pool_by_id
from database.orm_query_media_block import get_videos_id_from_block_session_pool, get_photos_id_from_block_session_pool
from keyboards.admin.inline_admin import get_inline
from keyboards.user.reply_user import start_kb


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