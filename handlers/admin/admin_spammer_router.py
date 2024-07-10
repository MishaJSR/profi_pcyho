from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InputMediaPhoto, InputMediaVideo, FSInputFile

from database.orm_query import get_all_users
from keyboards.user.reply_user import start_kb
from keyboards.admin.reply_admin import start_kb, answers_kb_end, reset_kb, send_img_kb
from handlers.admin.states import Admin_state, AdminStateSender

import os
import uuid

admin_spammer_router = Router()
destination_path = os.getcwd() + '\downloads'


@admin_spammer_router.message(F.text == 'Отправить рассылку')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Напишите текст рассылки', reply_markup=reset_kb())
    await state.set_state(AdminStateSender.text_state)


@admin_spammer_router.message(AdminStateSender.text_state)
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminStateSender.text = message.text
    await message.answer(text='Отправьте изображение', reply_markup=send_img_kb())
    await state.set_state(AdminStateSender.image_state)


@admin_spammer_router.message(AdminStateSender.image_state)
async def process_photo(message: types.Message, state: FSMContext):
    # if message.text == 'Оставить пустым':
    #     await message.answer(text=AdminStateSender.text, reply_markup=answers_kb_end())
    # else:
    #     await message.answer_photo(caption=AdminStateSender.text, photo=message.photo[-1].file_id,
    #                                reply_markup=answers_kb_end())
    #     AdminStateSender.photo = message.photo[-1].file_id
    await message.answer(text='Все верно?')
    await state.set_state(AdminStateSender.confirm_state)


@admin_spammer_router.message(AdminStateSender.confirm_state)
async def get_photo(message: types.Message):
    unique_photo_name = None
    unique_video_name = None
    try:
        if message.photo:
            unique_photo_name = str(uuid.uuid4())
            await message.bot.download(file=message.photo[-1].file_id,
                                       destination=destination_path + f"/{unique_photo_name}.jpg")
        if message.video:
            video = message.video
            file_id = video.file_id
            file = await message.bot.get_file(file_id)
            unique_video_name = str(uuid.uuid4())
            await message.bot.download_file(file.file_path, destination_path + f"/{unique_video_name}.mp4")
            photo_1 = InputMediaPhoto(type='photo',
                                      media=FSInputFile(destination_path + f"/image.jpg"),
                                      caption='Описание к медиагруппе')
            video1 = InputMediaVideo(type='video',
                                     media=FSInputFile(destination_path + f"/video.mp4"))
            media = [photo_1, video1]
            await message.answer_media_group(media=media)
    except Exception as e:
        print(e)


# @admin_spammer_router.message(AdminStateSender.confirm_state)
# async def process_photo(message: types.Message, session: AsyncSession, state: FSMContext):
#     try:
#         res = await get_all_users(session)
#         await message.answer(text="Начало рассылки")
#         for user in res:
#             await spammer(message, user, AdminStateSender)
#             # await message.bot.send_photo(chat_id=user._mapping['user_id'], photo=AdminStateSender.photo,
#             #                              caption=AdminStateSender.text)
#         await message.answer(text="Рассылка завершена", reply_markup=start_kb())
#     except:
#         await message.answer(text="Ошибка рассылки", reply_markup=start_kb())
#     await state.set_state(Admin_state.start)


async def spammer(message, user, state):
    pass
    # await message.bot.copy_message(548349299, 548349299, message.message_id)
    # if state.photo is None:
    #     await message.forward(user._mapping['user_id'])
    #     await message.bot.send_message(chat_id=user._mapping['user_id'], text=state.text)
    # else:
    #     await message.bot.send_photo(chat_id=user._mapping['user_id'], photo=state.photo, caption=state.text)