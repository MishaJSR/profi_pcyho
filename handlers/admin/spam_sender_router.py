from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Block
from database.orm_query import find_task, delete_task
from database.orm_query_block import get_block_active, get_block_by_id
from database.orm_query_media_block import get_videos_id_from_block, get_photos_id_from_block
from keyboards.admin.inline_admin import get_inline
from keyboards.user.reply_user import start_kb
from keyboards.admin.reply_admin import start_kb, reset_kb, spam_actions_kb
from handlers.admin.states import AdminManageTaskState, AdminStateDelete, AdminStateSpammer

spam_sender_router = Router()


@spam_sender_router.message(F.text == 'Рассылка')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer('Выберите действие', reply_markup=spam_actions_kb())
    await state.set_state(AdminStateSpammer.spam_actions)


@spam_sender_router.message(AdminStateSpammer.spam_actions, F.text == 'Отобразить статус блоков')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_block_active(session)
        for row in res:
            rus_date = row._data[0].date_to_post.strftime("%d.%m.%Y %H:%M")
            await message.answer(f"{row._data[0].block_name}\n"
                                 f"Выслано {row._data[0].count_send} раз\n"
                                 f"Дата постинга: {rus_date}\n")
    except Exception as e:
        await message.answer('Ошибка при попытке подключения к базе данных', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return


@spam_sender_router.message(AdminStateSpammer.spam_actions, F.text == 'Тестовая рассылка')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        block = await get_block_by_id(session, block_id=6)
        rus_date = block._data[0].date_to_post.strftime("%d.%m.%Y %H:%M")
        await message.answer(f"{block._data[0].block_name}\n"
                             f"Выслано {block._data[0].count_send} раз\n"
                             f"Дата постинга: {rus_date}\n")
        content = block._data[0].content
        callback = block._data[0].callback_button_id
        block_id = block._data[0].id

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
        await message.answer_media_group(media=media_group)
        await message.answer_video(video=video_content[0], reply_markup=get_inline(callback_data=callback))


    except Exception as e:
        await message.answer(f'Ошибка при попытке подключения к базе данных {e}', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return