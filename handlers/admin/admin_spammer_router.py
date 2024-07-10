from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InputMediaPhoto, InputMediaVideo, FSInputFile

from database.orm_query import get_all_users
from keyboards.user.reply_user import start_kb
from keyboards.admin.reply_admin import start_kb, answers_kb_end, reset_kb, send_img_kb, send_video_kb, \
    send_video_repeat_kb, send_img_repeat_kb, prepare_to_spam, send_media_kb
from handlers.admin.states import Admin_state, AdminStateSender

import os
import uuid

admin_spammer_router = Router()
destination_path = os.getcwd() + '\downloads'


@admin_spammer_router.message(F.text == 'Отправить рассылку')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Напишите текст рассылки', reply_markup=reset_kb())
    await state.set_state(AdminStateSender.text_state)


@admin_spammer_router.message(StateFilter('*'), F.text == 'Подготовить сообщение к рассылке')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer_media_group(media=AdminStateSender.media)
    for file_id in AdminStateSender.video_id_list:
        await message.bot.send_video(548349299, video=file_id)
    await message.answer(text='Все верно?', reply_markup=prepare_to_spam())
    await state.set_state(AdminStateSender.confirm_state)


@admin_spammer_router.message(AdminStateSender.text_state)
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminStateSender.text = message.text
    await message.answer(text='Отправьте медиафайл', reply_markup=send_media_kb())
    AdminStateSender.media = []
    AdminStateSender.video_id_list = []
    AdminStateSender.photo_counter = 0
    await state.set_state(AdminStateSender.media_state)


@admin_spammer_router.message(AdminStateSender.media_state)
async def fill_admin_state(message: types.Message, state: FSMContext):
    try:
        if message.photo:
            if AdminStateSender.photo_counter == 0:
                AdminStateSender.media.append(InputMediaPhoto(type='photo', media=message.photo[-1].file_id,
                                                              caption=AdminStateSender.text))
            else:
                AdminStateSender.media.append(InputMediaPhoto(type='photo', media=message.photo[-1].file_id))
            AdminStateSender.photo_counter += 1
        if message.video:
            video = message.video
            file_id = video.file_id
            AdminStateSender.video_id_list.append(file_id)
    except Exception as e:
        print(e)


@admin_spammer_router.message(AdminStateSender.confirm_state)
async def get_photo(message: types.Message, state: FSMContext):
    await message.bot.send_video(message.chat.id, video=AdminStateSender.video_id)
    await message.answer('Укажите краткое название блока', reply_markup=reset_kb())
    await state.set_state(AdminStateSender.name_block)


@admin_spammer_router.message(AdminStateSender.name_block, F.text)
async def get_photo(message: types.Message, state: FSMContext):
    await message.answer('Блок загружен', reply_markup=reset_kb())
    # await state.set_state(AdminStateSender.sta)


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
