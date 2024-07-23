import emoji
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_block import get_block_for_add_task, get_block_by_block_name
from database.orm_query_block_pool import get_block_pool_all
from database.orm_query_block_pool_media import get_videos_id_from_block_pool, get_photos_id_from_block_pool
from database.orm_query_media_block import get_videos_id_from_block_session_pool, get_videos_id_from_block, \
    get_photos_id_from_block
from database.orm_query_media_task import add_media_task, get_media_task_by_task_id
from database.orm_query_task import add_task_image, add_task_test, get_task_for_delete, delete_task, \
    get_task_by_block_id
from database.orm_superuser import set_backup
from keyboards.admin.inline_admin import get_inline
from keyboards.admin.reply_admin import start_kb, back_kb, type_task_kb, block_pool_kb, send_spam, test_actions, \
    list_task_to_delete, send_media_kb, send_media_kb_task, show_block_or_test, spam_actions_kb
from handlers.admin.states import AdminManageTaskState, AdminStatePreShow

admin_show_block_router = Router()

@admin_show_block_router.message(StateFilter(AdminStatePreShow), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    print(current_state)

    if current_state == AdminStatePreShow.choose_block_or_test:
        await message.answer(text='Выберите блок для предпросмотра',
                         reply_markup=block_pool_kb(data=AdminStatePreShow.block_pool))
        await state.set_state(AdminStatePreShow.choose_block)
        return

    if current_state == AdminStatePreShow.start:
        await message.answer(text='Выберите действие', reply_markup=spam_actions_kb())
        return

    previous = None
    for step in AdminStatePreShow.__all_states__:
        if step.state == current_state:
            print(current_state)
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому шагу \n{AdminStatePreShow.texts[previous.state][0]}",
                                 reply_markup=AdminStatePreShow.texts[previous.state][1]())
            return
        previous = step


@admin_show_block_router.message(F.text == 'Предпросмотр')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminStatePreShow.block_pool = []
    blocks = await get_block_for_add_task(session)
    AdminStatePreShow.block_pool = [block._data[0].block_name for block in blocks]
    await message.answer("Выберите блок для предпросмотра",
                         reply_markup=block_pool_kb(data=AdminStatePreShow.block_pool))
    await state.set_state(AdminStatePreShow.choose_block)


@admin_show_block_router.message(F.text == 'Предпросмотр')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminStatePreShow.block_pool = []
    blocks = await get_block_for_add_task(session)
    AdminStatePreShow.block_pool = [block._data[0].block_name for block in blocks]
    await message.answer("Выберите блок для предпросмотра",
                         reply_markup=block_pool_kb(data=AdminStatePreShow.block_pool))
    await state.set_state(AdminStatePreShow.choose_block)


@admin_show_block_router.message(AdminStatePreShow.choose_block, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminStatePreShow.block_name = message.text
    block = await get_block_by_block_name(session, block_name=AdminStatePreShow.block_name)
    AdminStatePreShow.block_id = block._data[0].id
    if not block:
        await message.answer("Не могу найти блок\nПовторите попытку",
                             reply_markup=block_pool_kb(data=AdminStatePreShow.block_pool))
        return
    await message.answer("Выберите что хотите посмотреть в блоке", reply_markup=show_block_or_test())
    await state.set_state(AdminStatePreShow.choose_block_or_test)


@admin_show_block_router.message(AdminStatePreShow.choose_block_or_test, F.text == "Содержание блока")
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        user_id = message.from_user.id
        block = await get_block_by_block_name(session, block_name=AdminStatePreShow.block_name)
        if not block:
            await message.answer("Не могу найти блок", reply_markup=start_kb())
            await state.set_state(AdminStatePreShow.start)
            return
        content = block._data[0].content
        callback = block._data[0].callback_button_id
        block_id = block._data[0].id
        tasks = await get_task_for_delete(session, task_id=block_id)
        has_tasks = True
        if len(tasks) == 0:
            has_tasks = False
        if block._data[0].is_sub_block:
            await send_multi_post_test(message.bot, session, user_id=user_id, block_id=block_id)
            return
        if not block._data[0].has_media:
            await message.bot.send_message(chat_id=user_id, text=content)
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
            await message.bot.send_media_group(user_id, media=media_group)
        if video_content:
            for index, video_id in enumerate(video_content):
                await message.bot.send_video(user_id, video=video_id)

    except Exception as e:
        await message.bot.send_message(chat_id=548349299, text=f'Ошибка при попытке подключения к базе данных {e}',
                                       reply_markup=start_kb())
        return


@admin_show_block_router.message(AdminStatePreShow.choose_block_or_test, F.text == "Содержание теста")
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    tasks = await get_task_by_block_id(session, block_id=AdminStatePreShow.block_id)
    if not tasks:
        await message.answer("Тестов в блоке нет")
        return
    for task in tasks:
        task_id = task._data[0].id
        if not task._data[0].answer_mode == "Тест":
            continue
        photos_ids = await get_media_task_by_task_id(session, task_id=task_id)
        text_to_send = get_text_to_send(task)
        if not photos_ids:
            await message.answer(text_to_send, parse_mode="Markdown")
        else:
            await send_task_with_media(message, session, photos_ids, text_to_send)


async def send_task_with_media(message, session, photos_ids, text_to_send):
    media = []
    for index, photos_id in enumerate(photos_ids):
        if index == 0:
            media.append(InputMediaPhoto(type='photo', media=photos_id[0], caption=text_to_send, parse_mode="Markdown"))
        else:
            media.append(InputMediaPhoto(type='photo', media=photos_id[0]))
    await message.answer_media_group(media=media)


def get_text_to_send(task) -> str:
    answers_text = ""
    addition_text = ""
    addition = task._data[0].addition
    if not addition:
        addition_text = addition
    answers_pool = task._data[0].answers.split("`")
    for answer in answers_pool:
        answers_text += answer + "\n"
    text_to_send = f"{task._data[0].description}\n\n{answers_text}\n\n{addition_text}"
    return text_to_send


async def send_multi_post_test(bot, session, user_id, block_id):
    block_pool = await get_block_pool_all(session, block_main_id=block_id)
    for block in block_pool:
        content = block._data[0].content
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
