from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_block import add_block, get_block_for_add_task, delete_block
from database.orm_query_media_block import add_media
from keyboards.admin.inline_admin import get_inline
from keyboards.admin.reply_admin import reset_kb, prepare_to_spam, send_media_kb, send_media_check_kb, start_kb, \
    block_actions, block_pool_kb
from handlers.admin.states import AdminManageTaskState, AdminManageBlockState
import logging
import uuid
import datetime

admin_block_router = Router()


@admin_block_router.message(StateFilter(AdminManageBlockState), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    print(current_state)

    if current_state == AdminManageBlockState.start:
        await message.answer('Предыдущего шага нет')
        return

    if current_state == AdminManageBlockState.confirm_state or current_state == AdminManageBlockState.date_posting:
        await message.answer(text='Отправьте медиафайл', reply_markup=send_media_kb())
        AdminManageBlockState.media = []
        AdminManageBlockState.video_id_list = []
        await state.set_state(AdminManageBlockState.media_state)
        return

    if current_state == AdminManageBlockState.choose_block_actions:
        await message.answer(text='Выберите необходимое действие', reply_markup=start_kb())
        await state.set_state(AdminManageBlockState.start)
        return

    if current_state == AdminManageBlockState.choose_block_to_delete:
        await message.answer(text='Выберите необходимое действие', reply_markup=block_actions())
        await state.set_state(AdminManageBlockState.choose_block_actions)
        return



    previous = None
    for step in AdminManageBlockState.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому шагу \n{AdminManageBlockState.texts[previous.state][0]}",
                                 reply_markup=AdminManageBlockState.texts[previous.state][1]())
            return
        previous = step


@admin_block_router.message(F.text == 'Управление блоками')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Выберите необходимое действие', reply_markup=block_actions())
    await state.set_state(AdminManageBlockState.choose_block_actions)


# @admin_block_router.callback_query()
# async def check_button(call: types.CallbackQuery):
#     print("call")
#     await call.message.answer("Hi! This is the first inline keyboard button.")
#     await call.answer('Вы выбрали каталог')
#     #9fa7e998-1700-46c9-8c8f-a82bd2fa4568


@admin_block_router.message(AdminManageBlockState.choose_block_actions, F.text == 'Добавить блок')
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminManageBlockState.text = None
    await message.answer(text='Напишите текст рассылки', reply_markup=reset_kb())
    await state.set_state(AdminManageBlockState.text_state)


'''Add block'''


@admin_block_router.message(AdminManageBlockState.text_state)
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminManageBlockState.text = message.text
    await message.answer(text='Отправьте медиафайл', reply_markup=send_media_kb())
    AdminManageBlockState.media = []
    AdminManageBlockState.video_id_list = []
    AdminManageBlockState.photo_counter = 0
    AdminManageBlockState.callback_for_task = None
    await state.set_state(AdminManageBlockState.media_state)


@admin_block_router.message(AdminManageBlockState.media_state)
async def fill_admin_state(message: types.Message, state: FSMContext):
    if message.text == 'Оставить пустым':
        await message.answer("Вы оставили поле пустым", reply_markup=send_media_check_kb())
        await state.set_state(AdminManageBlockState.prepare_to_load)
        return
    if not (message.video or message.photo):
        await message.answer("Ошбика ввода, необходимо отправить медиафайл")
        return
    try:
        if message.photo:
            if AdminManageBlockState.photo_counter == 0:
                AdminManageBlockState.media.append(InputMediaPhoto(type='photo', media=message.photo[-1].file_id,
                                                                   caption=AdminManageBlockState.text))
            else:
                AdminManageBlockState.media.append(InputMediaPhoto(type='photo', media=message.photo[-1].file_id))
            AdminManageBlockState.photo_counter += 1
            await message.answer("Медиафайл получен", reply_markup=send_media_check_kb())
        if message.video:
            video = message.video
            file_id = video.file_id
            AdminManageBlockState.video_id_list.append(file_id)
            await message.answer("Медиафайл получен", reply_markup=send_media_check_kb())
        await state.set_state(AdminManageBlockState.prepare_to_load)
    except Exception as e:
        await message.answer("Ошибка при получении медиафайла")


@admin_block_router.message(AdminManageBlockState.prepare_to_load, F.text == 'Подготовить сообщение к рассылке')
async def fill_admin_state(message: types.Message, state: FSMContext):
    if not AdminManageBlockState.media:
        await message.answer(f"{AdminManageBlockState.text}")
    else:
        if not AdminManageBlockState.video_id_list:
            AdminManageBlockState.callback_for_task = str(uuid.uuid4())
            await message.answer_media_group(media=AdminManageBlockState.media,
                                             reply_markup=get_inline(AdminManageBlockState.callback_for_task))
        else:
            await message.answer_media_group(media=AdminManageBlockState.media)
    for index, file_id in enumerate(AdminManageBlockState.video_id_list):
        if index == len(AdminManageBlockState.video_id_list) - 1:
            AdminManageBlockState.callback_for_task = str(uuid.uuid4())
            await message.answer_video(video=file_id,
                                       reply_markup=get_inline(AdminManageBlockState.callback_for_task))
        else:
            await message.answer_video(video=file_id)
    await message.answer(text='Все верно?', reply_markup=prepare_to_spam())
    await state.set_state(AdminManageBlockState.confirm_state)


@admin_block_router.message(AdminManageBlockState.confirm_state)
async def get_photo(message: types.Message, state: FSMContext):
    AdminManageBlockState.date_to_posting = None
    await message.answer('Укажите дату постинга в формате 11.02.2025.10.00', reply_markup=reset_kb())
    await state.set_state(AdminManageBlockState.date_posting)


@admin_block_router.message(AdminManageBlockState.date_posting, F.text)
async def get_photo(message: types.Message, state: FSMContext):
    AdminManageBlockState.date_to_posting = message.text
    await message.answer('Укажите уникальное название блока. Это название будет видно только вам',
                         reply_markup=reset_kb())
    await state.set_state(AdminManageBlockState.name_block)


@admin_block_router.message(AdminManageBlockState.name_block, F.text)
async def get_photo(message: types.Message, session: AsyncSession, state: FSMContext):
    await message.answer('Загрузка блока', reply_markup=reset_kb())
    block = message.text
    has_media = False
    print(block)
    text = AdminManageBlockState.text
    print(text)
    for photo in AdminManageBlockState.media:
        print(photo.media)
    for video_id in AdminManageBlockState.video_id_list:
        print(video_id)
    if AdminManageBlockState.media or AdminManageBlockState.video_id_list:
        has_media = True
    callback = AdminManageBlockState.callback_for_task
    d, m, y, h, minute = AdminManageBlockState.date_to_posting.split('.')
    date_to_post = datetime.datetime(year=int(y), month=int(m), day=int(d), hour=int(h), minute=int(minute))
    try:
        block_id = await add_block(session, block_name=block, content=text, has_media=has_media,
                                   date_to_post=date_to_post, progress_block=None, callback_button_id=callback)

        for photo in AdminManageBlockState.media:
            await add_photo_pool(session, block_id, photo.media)
        for video_id in AdminManageBlockState.video_id_list:
            await add_video_pool(session, block_id, video_id)
        await message.answer(f'Блок {block} загружен', reply_markup=start_kb())
    except Exception as e:
        logging.info(e)
        await message.answer('Ошибка загрузки', reply_markup=start_kb())
        return
    await state.set_state(AdminManageBlockState.start)


async def add_photo_pool(session, block_id, file_id):
    await add_media(session, block_id=block_id, photo_id=file_id)


async def add_video_pool(session, block_id, file_id):
    await add_media(session, block_id=block_id, video_id=file_id)


'''Add block'''

'''delete block'''


@admin_block_router.message(AdminManageBlockState.choose_block_actions, F.text == 'Удалить блок')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_block_for_add_task(session)
    except Exception as e:
        await message.answer('Ошибка подключения к базе данных блоков. Возможно у вас отсутствуют блоки')
        return
    AdminManageBlockState.block_list = []
    for block in res:
        AdminManageBlockState.block_list.append(block._data[0].block_name)
        AdminManageBlockState.block_dict_id[block._data[0].block_name] = block._data[0].id
    await message.answer(text='Выберите какой из блоков вы хотите удалить', reply_markup=block_pool_kb(AdminManageBlockState.block_list))
    await state.set_state(AdminManageBlockState.choose_block_to_delete)


@admin_block_router.message(AdminManageBlockState.choose_block_to_delete, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminManageBlockState.block_id = AdminManageBlockState.block_dict_id.get(message.text)
    if not AdminManageBlockState.block_id:
        await message.answer(f'Такой блок не найден', reply_markup=start_kb())
        return
    try:
        res = await delete_block(session, block_id=AdminManageBlockState.block_id)
        await message.answer("Блок удален", reply_markup=start_kb())
    except Exception as e:
        await message.answer('Такой блок не найден', reply_markup=start_kb())
    finally:
        await state.set_state(AdminManageBlockState.start)


'''delete block'''


# @admin_block_router.message(AdminStateSender.confirm_state)
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


async def get_generator(arr: list):
    for item in arr:
        yield item
