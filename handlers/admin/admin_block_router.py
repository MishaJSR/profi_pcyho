from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from aiogram.types import InputMediaPhoto

from keyboards.admin.inline_admin import get_inline
from keyboards.admin.reply_admin import reset_kb, prepare_to_spam, send_media_kb, send_media_check_kb, start_kb, \
    block_actions
from handlers.admin.states import Admin_state, AdminStateSender
import logging
import uuid

admin_block_router = Router()


@admin_block_router.message(StateFilter(AdminStateSender), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AdminStateSender.start:
        await message.answer('Предыдущего шага нет')
        return

    if current_state == AdminStateSender.confirm_state:
        await message.answer(text='Отправьте медиафайл', reply_markup=send_media_kb())
        AdminStateSender.media = []
        AdminStateSender.video_id_list = []
        await state.set_state(AdminStateSender.media_state)
        return

    previous = None
    for step in AdminStateSender.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому шагу \n{AdminStateSender.texts[previous.state][0]}",
                                 reply_markup=AdminStateSender.texts[previous.state][1]())
            return
        previous = step


@admin_block_router.message(F.text == 'Управление блоками')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Выберите необходимое действие', reply_markup=block_actions())
    await state.set_state(AdminStateSender.choose_block_actions)


# @admin_block_router.callback_query()
# async def check_button(call: types.CallbackQuery):
#     print("call")
#     await call.message.answer("Hi! This is the first inline keyboard button.")
#     await call.answer('Вы выбрали каталог')
#     #9fa7e998-1700-46c9-8c8f-a82bd2fa4568


@admin_block_router.message(AdminStateSender.choose_block_actions, F.text == 'Добавить блок')
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminStateSender.text = None
    await message.answer(text='Напишите текст рассылки', reply_markup=reset_kb())
    await state.set_state(AdminStateSender.text_state)


'''Add block'''


@admin_block_router.message(AdminStateSender.text_state)
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminStateSender.text = message.text
    await message.answer(text='Отправьте медиафайл', reply_markup=send_media_kb())
    AdminStateSender.media = []
    AdminStateSender.video_id_list = []
    AdminStateSender.photo_counter = 0
    AdminStateSender.callback_for_task = None
    await state.set_state(AdminStateSender.media_state)


@admin_block_router.message(AdminStateSender.media_state)
async def fill_admin_state(message: types.Message, state: FSMContext):
    if message.text == 'Оставить пустым':
        await message.answer("Вы оставили поле пустым", reply_markup=send_media_check_kb())
        await state.set_state(AdminStateSender.prepare_to_load)
        return
    if not (message.video or message.photo):
        await message.answer("Ошбика ввода, необходимо отправить медиафайл")
        return
    try:
        if message.photo:
            if AdminStateSender.photo_counter == 0:
                AdminStateSender.media.append(InputMediaPhoto(type='photo', media=message.photo[-1].file_id,
                                                              caption=AdminStateSender.text))
            else:
                AdminStateSender.media.append(InputMediaPhoto(type='photo', media=message.photo[-1].file_id))
            AdminStateSender.photo_counter += 1
            await message.answer("Медиафайл получен", reply_markup=send_media_check_kb())
        if message.video:
            video = message.video
            file_id = video.file_id
            AdminStateSender.video_id_list.append(file_id)
            await message.answer("Медиафайл получен", reply_markup=send_media_check_kb())
        await state.set_state(AdminStateSender.prepare_to_load)
    except Exception as e:
        await message.answer("Ошибка при получении медиафайла")


@admin_block_router.message(AdminStateSender.prepare_to_load, F.text == 'Подготовить сообщение к рассылке')
async def fill_admin_state(message: types.Message, state: FSMContext):
    if not AdminStateSender.media:
        await message.answer(f"{AdminStateSender.text}")
    else:
        if not AdminStateSender.video_id_list:
            AdminStateSender.callback_for_task = str(uuid.uuid4())
            await message.answer_media_group(media=AdminStateSender.media,
                                             reply_markup=get_inline(AdminStateSender.callback_for_task))
        else:
            await message.answer_media_group(media=AdminStateSender.media)
    for index, file_id in enumerate(AdminStateSender.video_id_list):
        if index == len(AdminStateSender.video_id_list) - 1:
            AdminStateSender.callback_for_task = str(uuid.uuid4())
            await message.bot.send_video(548349299, video=file_id,
                                         reply_markup=get_inline(AdminStateSender.callback_for_task))
        else:
            await message.bot.send_video(548349299, video=file_id)
    await message.answer(text='Все верно?', reply_markup=prepare_to_spam())
    await state.set_state(AdminStateSender.confirm_state)


@admin_block_router.message(AdminStateSender.confirm_state)
async def get_photo(message: types.Message, state: FSMContext):
    await message.answer('Укажите краткое название блока', reply_markup=reset_kb())
    await state.set_state(AdminStateSender.name_block)


@admin_block_router.message(AdminStateSender.name_block, F.text)
async def get_photo(message: types.Message, state: FSMContext):
    await message.answer('Загрузка блока', reply_markup=reset_kb())
    block = message.text
    print(block)
    text = AdminStateSender.text
    print(text)
    for photo in AdminStateSender.media:
        print(photo.media)
    for video_id in AdminStateSender.video_id_list:
        print(video_id)
    callback = AdminStateSender.callback_for_task
    print(callback)

    await message.answer(f'Блок {block} загружен', reply_markup=start_kb())
    # await state.set_state(AdminStateSender.sta)


'''Add block'''

'''delete block'''


@admin_block_router.message(AdminStateSender.choose_block_actions, F.text == 'Удалить блок')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text='Выберите какой из блоков вы хотите удалить', reply_markup=reset_kb())
    await state.set_state(AdminStateSender.choose_block_actions)


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
