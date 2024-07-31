import datetime

from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_block.orm_query_block import get_block_active, get_block_names_all_not_past, get_date_post_block_by_name, \
    set_date_post_block_by_name
from database.orm_task.orm_query_task import get_task_by_block_id
from database.orm_user.orm_query_user import get_all_users_id_progress
from keyboards.admin.reply_admin import start_kb, spam_actions_kb, block_pool_kb, back_kb, send_media_vebinar, \
    send_media_kb_veb, send_spam, reset_kb
from handlers.admin.states import AdminStateSpammer

admin_manage_sender_router = Router()


@admin_manage_sender_router.message(StateFilter(AdminStateSpammer), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AdminStateSpammer.start:
        AdminStateSpammer.blocks_name = []
        AdminStateSpammer.name_of_block = None
        await message.answer(text='Выберите действие',
                             reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.start)
        return

    if current_state == AdminStateSpammer.set_text_spam or current_state == AdminStateSpammer.set_text_vebinar \
            or current_state == AdminStateSpammer.send_vebinar or current_state == AdminStateSpammer.set_image_vebinar \
            or current_state == AdminStateSpammer.prepare_to_load_img or current_state == AdminStateSpammer.set_veb_vebinar:
        AdminStateSpammer.web_vebinar = None
        AdminStateSpammer.discription_vebinar = None
        await message.answer(text='Выберите действие',
                             reply_markup=spam_actions_kb())
        await state.set_state(AdminStateSpammer.start)
        return

    if current_state == AdminStateSpammer.choose_block:
        AdminStateSpammer.blocks_name = []
        AdminStateSpammer.name_of_block = None
        await message.answer(text='Выберите действие',
                             reply_markup=spam_actions_kb())
        await state.set_state(AdminStateSpammer.start)
        return

    if current_state == AdminStateSpammer.spam_actions:
        AdminStateSpammer.blocks_name = []
        AdminStateSpammer.name_of_block = None
        await message.answer(text='Выберите действие',
                             reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.start)
        return

    if current_state == AdminStateSpammer.confirm_date:
        AdminStateSpammer.name_of_block = None
        await message.answer(text='Выберите блок',
                             reply_markup=block_pool_kb(AdminStateSpammer.blocks_name))
        await state.set_state(AdminStateSpammer.choose_block)
        return


@admin_manage_sender_router.message(F.text == 'Рассылка')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer('Выберите действие', reply_markup=spam_actions_kb())
    await state.set_state(AdminStateSpammer.spam_actions)


@admin_manage_sender_router.message(StateFilter(AdminStateSpammer), F.text == 'Отобразить статус блоков')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_block_active(session)

        for row in res:
            rus_date = row.date_to_post.strftime("%d.%m.%Y %H:%M")
            tasks = await get_task_by_block_id(session, block_id=row.id)
            await message.answer(f"{row.block_name}\n"
                                 f"Выслано {row.count_send} раз\n"
                                 f"Дата постинга: {rus_date}\n"
                                 f"Заданий добавлено: {len(tasks)}\n")
    except Exception as e:
        await message.answer('Ошибка при попытке подключения к базе данных', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return


@admin_manage_sender_router.message(StateFilter(AdminStateSpammer), F.text == 'Изменить дату рассылки')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        blocks = await get_block_names_all_not_past(session)
        AdminStateSpammer.blocks_name = []
        AdminStateSpammer.name_of_block = None
        for block in blocks:
            AdminStateSpammer.blocks_name.append(block[0])
        if not AdminStateSpammer.blocks_name:
            await message.answer(f'Возможно у вас отсутствуют блоки с возможностью редактирования даты',
                                 reply_markup=start_kb())
            return
        await message.answer("Выберите блок", reply_markup=block_pool_kb(AdminStateSpammer.blocks_name))
        await state.set_state(AdminStateSpammer.choose_block)

    except Exception as e:
        print(e)
        await message.answer(f'Ошибка при попытке подключения к базе данных\n'
                             f'Возможно у вас отсутствуют блоки с возможностью редактирования даты',
                             reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return

@admin_manage_sender_router.message(AdminStateSpammer.choose_block, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        AdminStateSpammer.name_of_block = message.text
        date_post = await get_date_post_block_by_name(session, block_name=AdminStateSpammer.name_of_block)
        date_post = date_post[0].strftime("%d.%m.%Y")
        await message.answer(
            "Пожалуйста выберите дату: ",
            reply_markup=await SimpleCalendar(locale=await get_user_locale(message.from_user)).start_calendar()
        )
        await message.answer(f'Прошлая дата публикации блока {date_post}', reply_markup=back_kb())
        await state.set_state(AdminStateSpammer.confirm_date)

    except Exception as e:
        await message.answer("Ошибка, неправильный формат даты\nПовторите ввод")
        return


@admin_manage_sender_router.message(F.text == 'Отправить спам')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminStateSpammer.discription_vebinar = None
    await message.answer("Введите описание рассылки", reply_markup=back_kb())
    await state.set_state(AdminStateSpammer.set_text_vebinar)


@admin_manage_sender_router.message(StateFilter(AdminStateSpammer.set_text_vebinar), F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminStateSpammer.discription_vebinar = message.text
    AdminStateSpammer.media = []
    await message.answer("Отправьте медиафайлы, кроме видео", reply_markup=send_media_kb_veb())
    await state.set_state(AdminStateSpammer.set_image_vebinar)


@admin_manage_sender_router.message(StateFilter(AdminStateSpammer.set_image_vebinar))
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text == 'Оставить пустым':
        await message.answer("Вы оставили поле пустым", reply_markup=send_media_vebinar())
        await state.set_state(AdminStateSpammer.prepare_to_load_img)
        return
    if not message.photo:
        await message.answer("Ошбика ввода, необходимо отправить медиафайл")
        return
    try:
        if message.photo:
            if AdminStateSpammer.photo_counter == 0:
                AdminStateSpammer.media.append(InputMediaPhoto(type='photo', media=message.photo[-1].file_id,
                                                               caption=AdminStateSpammer.discription_vebinar))
            else:
                AdminStateSpammer.media.append(InputMediaPhoto(type='photo', media=message.photo[-1].file_id))
            AdminStateSpammer.photo_counter += 1
            await message.answer("Медиафайл получен", reply_markup=send_media_vebinar())
        await state.set_state(AdminStateSpammer.prepare_to_load_img)
    except Exception as e:
        await message.answer(f"{e}Ошибка при получении медиафайла")


@admin_manage_sender_router.message(StateFilter(AdminStateSpammer.prepare_to_load_img),
                                    F.text == "Подготовить спам к рассылке")
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        if not AdminStateSpammer.media:
            await message.answer(f"{AdminStateSpammer.discription_vebinar}")
            await message.answer("Все верно?", reply_markup=send_spam())
            await state.set_state(AdminStateSpammer.set_veb_vebinar)
        else:
            await message.answer_media_group(media=AdminStateSpammer.media)
            await message.answer("Все верно?", reply_markup=send_spam())
            await state.set_state(AdminStateSpammer.set_veb_vebinar)
    except Exception as e:
        await message.answer("Ошибка при получении медиафайла")


@admin_manage_sender_router.message(AdminStateSpammer.set_veb_vebinar, F.text == "Подтвердить")
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    count_send = 0
    try:
        await message.answer("Начало рассылки")
        users = await get_all_users_id_progress(session)
        for user in users:
            if AdminStateSpammer.media:
                await message.bot.send_media_group(chat_id=user._data[0], media=AdminStateSpammer.media)
            else:
                await message.bot.send_message(chat_id=user._data[0], text=AdminStateSpammer.discription_vebinar)
            count_send += 1
        await message.answer(f"Успешная рассылка. Выслано {count_send} пользователям", reply_markup=spam_actions_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
    except Exception as e:
        await message.answer(f'{e} Ошибка при попытке подключения к базе данных', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return
    await state.set_state(AdminStateSpammer.start)





@admin_manage_sender_router.callback_query(SimpleCalendarCallback.filter(), StateFilter(AdminStateSpammer))
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData,
                                  session: AsyncSession, state: FSMContext):
    if not AdminStateSpammer.name_of_block:
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
    if datetime.datetime.now() > datetime.datetime(year=callback_data.year,
                                                   month=callback_data.month,
                                                   day=callback_data.day):
        await callback_query.message.answer("Невозможно установить дату которая раньше текущего дня")
        return
    if not date:
        date = datetime.datetime.now()
        selected = True

    if selected:
        await callback_query.message.answer(
            f'Вы выбрали {date.strftime("%d.%m.%Y")}',
            reply_markup=start_kb()
        )
    AdminStateSpammer.date_change = date
    await callback_query.message.answer('Укажите время постинга в формате 09.00', reply_markup=reset_kb())



@admin_manage_sender_router.message(AdminStateSpammer.confirm_date, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        hour_to_post = int(message.text.split(".")[0])
        minute_to_post = int(message.text.split(".")[1])
        AdminStateSpammer.date_change = AdminStateSpammer.date_change.replace(hour=hour_to_post, minute=minute_to_post)
        await set_date_post_block_by_name(session, block_name=AdminStateSpammer.name_of_block,
                                          date_to_post=AdminStateSpammer.date_change)
        await message.answer('Изменение успешно применено', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)

    except Exception as e:
        await message.answer('Ошибка при попытке подключения к базе данных', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return