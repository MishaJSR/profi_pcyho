from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext

from aiogram.types import InputMediaPhoto, CallbackQuery, ReplyKeyboardRemove
from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_block import add_block, delete_block, get_order_block, \
    set_progres_block, get_block_for_delete
from database.orm_query_media_block import add_media
from keyboards.admin.inline_admin import get_inline
from keyboards.admin.reply_admin import reset_kb, prepare_to_spam, send_media_kb, send_media_check_kb, start_kb, \
    block_actions, block_pool_kb, back_kb
from handlers.admin.states import AdminManageBlockState
import logging
import uuid
import datetime

admin_block_router = Router()


@admin_block_router.message(StateFilter(AdminManageBlockState), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AdminManageBlockState.start:
        await message.answer('Предыдущего шага нет')
        return

    if current_state == AdminManageBlockState.confirm_state or current_state == AdminManageBlockState.date_posting:
        AdminManageBlockState.callback_for_task = None
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

    if current_state == AdminManageBlockState.name_block or current_state == AdminManageBlockState.time_block:
        await message.answer(
            "Пожалуйста выберите дату: ",
            reply_markup=await SimpleCalendar(locale=await get_user_locale(message.from_user)).start_calendar()
        )
        await state.set_state(AdminManageBlockState.date_posting)
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
    await state.set_state(AdminManageBlockState.media_state)


@admin_block_router.message(AdminManageBlockState.media_state)
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminManageBlockState.callback_for_task = None
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
    AdminManageBlockState.callback_for_task = None
    if not AdminManageBlockState.media:
        await message.answer(f"{AdminManageBlockState.text}")
    else:
        await message.answer_media_group(media=AdminManageBlockState.media)
    for index, file_id in enumerate(AdminManageBlockState.video_id_list):
        if index == len(AdminManageBlockState.video_id_list) - 1:
            await message.answer_video(video=file_id)
    await message.answer(text='Все верно?', reply_markup=prepare_to_spam())
    await state.set_state(AdminManageBlockState.confirm_state)


@admin_block_router.message(AdminManageBlockState.confirm_state, F.text == "Подтвердить")
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminManageBlockState.callback_for_task = str(uuid.uuid4())
    await message.answer(
        "Загрузка календаря",
        reply_markup=await SimpleCalendar(locale=await get_user_locale(message.from_user)).start_calendar()
    )
    await state.set_state(AdminManageBlockState.date_posting)
    await message.answer("Выберите дату постинга", reply_markup=back_kb())


@admin_block_router.callback_query(SimpleCalendarCallback.filter(), StateFilter(AdminManageBlockState))
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData,
                                  session: AsyncSession, state: FSMContext):
    if not AdminManageBlockState.callback_for_task:
        await callback_query.message.answer("Клавиатура неактивна")
        await callback_query.answer("Клавиатура неактивна")
        return
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime.datetime(2022, 1, 1), datetime.datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if 'DAY' not in callback_query.data:
        await callback_query.answer("...")
        return
    if not date:
        date = datetime.datetime.now()
    AdminManageBlockState.date_to_posting = date
    await callback_query.message.answer(f'Вы выбрали {date.strftime("%d.%m.%Y")}')
    await callback_query.answer("...")
    await callback_query.message.answer('Укажите время постинга в формате 09.00',
                                        reply_markup=reset_kb())
    await state.set_state(AdminManageBlockState.time_block)


@admin_block_router.message(AdminManageBlockState.time_block, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        hour_to_post = int(message.text.split(".")[0])
        minute_to_post = int(message.text.split(".")[1])
        AdminManageBlockState.date_to_posting = AdminManageBlockState.date_to_posting.replace(hour=hour_to_post,
                                                                                              minute=minute_to_post)
        await message.answer('Укажите уникальное название блока. Это название будет видно только вам',
                                            reply_markup=reset_kb())
        await state.set_state(AdminManageBlockState.name_block)
    except Exception as e:
        await message.answer("Ошибка, неправильный формат даты\nПовторите ввод")
        return


    await state.set_state(AdminManageBlockState.name_block)


@admin_block_router.message(AdminManageBlockState.name_block, F.text)
async def get_photo(message: types.Message, session: AsyncSession, state: FSMContext):
    await message.answer('Загрузка блока', reply_markup=reset_kb())
    block = message.text
    has_media = False
    text = AdminManageBlockState.text
    if AdminManageBlockState.media or AdminManageBlockState.video_id_list:
        has_media = True
    callback = AdminManageBlockState.callback_for_task
    try:
        block_id = await add_block(session, block_name=block, content=text, has_media=has_media,
                                   date_to_post=AdminManageBlockState.date_to_posting, progress_block=None,
                                   callback_button_id=callback, is_vebinar=False)
        for photo in AdminManageBlockState.media:
            await add_photo_pool(session, block_id, photo.media)
        for video_id in AdminManageBlockState.video_id_list:
            await add_video_pool(session, block_id, video_id)
    except Exception as e:
        logging.info(e)
        await message.answer(f'Ошибка загрузки {e}', reply_markup=start_kb())
        return
    await update_progress(message, session)
    await message.answer(f'Блок {block} загружен', reply_markup=start_kb())
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
        res = await get_block_for_delete(session)
    except Exception as e:
        await message.answer('Ошибка подключения к базе данных блоков. Возможно у вас отсутствуют блоки')
        return
    AdminManageBlockState.block_list = []
    for block in res:
        AdminManageBlockState.block_list.append(block._data[0].block_name)
        AdminManageBlockState.block_dict_id[block._data[0].block_name] = block._data[0].id
    await message.answer(text='Выберите какой из блоков вы хотите удалить',
                         reply_markup=block_pool_kb(AdminManageBlockState.block_list))
    await state.set_state(AdminManageBlockState.choose_block_to_delete)


@admin_block_router.message(AdminManageBlockState.choose_block_to_delete, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminManageBlockState.block_id = AdminManageBlockState.block_dict_id.get(message.text)
    if not AdminManageBlockState.block_id:
        await message.answer(f'Такой блок не найден', reply_markup=start_kb())
        return
    try:
        await delete_block(session, block_id=AdminManageBlockState.block_id)
        await update_progress(message, session)
        await message.answer("Блок удален", reply_markup=start_kb())
    except Exception as e:
        await message.answer('Такой блок не найден', reply_markup=start_kb())
    finally:
        await state.set_state(AdminManageBlockState.start)


'''delete block'''


async def update_progress(message, session):
    try:
        res = await get_order_block(session)
        for index, el in enumerate(res):
            if el._data[0].progress_block != index + 1:
                await set_progres_block(session, block_id=el._data[0].id, progress=index + 1)
    except Exception as e:
        await message.answer(e)


async def get_generator(arr: list):
    for item in arr:
        yield item
