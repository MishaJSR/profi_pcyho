import datetime

from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback, DialogCalendarCallback, \
    DialogCalendar
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_block import get_block_active, get_block_names_all, get_date_post_block_by_name, \
    set_date_post_block_by_name, get_next_block_progress
from database.orm_query_task import get_task_by_block_id
from database.orm_query_user import get_all_users_id, get_all_users_id_progress
from keyboards.admin.inline_admin import get_inline_vebinar
from keyboards.admin.reply_admin import start_kb, spam_actions_kb, block_pool_kb, back_kb
from handlers.admin.states import AdminStateSpammer

admin_manage_sender_router = Router()


@admin_manage_sender_router.message(StateFilter(AdminStateSpammer), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    print(current_state)

    if current_state == AdminStateSpammer.start:
        AdminStateSpammer.blocks_name = []
        AdminStateSpammer.name_of_block = None
        await message.answer(text='Выберите действие',
                             reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.start)
        return

    if current_state == AdminStateSpammer.set_text_spam or current_state == AdminStateSpammer.set_text_vebinar\
            or current_state == AdminStateSpammer.send_vebinar:
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
            rus_date = row._data[0].date_to_post.strftime("%d.%m.%Y %H:%M")
            tasks = await get_task_by_block_id(session, block_id=row._data[0].id)
            await message.answer(f"{row._data[0].block_name}\n"
                                 f"Выслано {row._data[0].count_send} раз\n"
                                 f"Дата постинга: {rus_date}\n"
                                 f"Заданий добавлено: {len(tasks)}\n")
    except Exception as e:
        await message.answer('Ошибка при попытке подключения к базе данных', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return


@admin_manage_sender_router.message(StateFilter(AdminStateSpammer), F.text == 'Изменить дату рассылки')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        blocks = await get_block_names_all(session)
        AdminStateSpammer.blocks_name = []
        AdminStateSpammer.name_of_block = None
        for block in blocks:
            AdminStateSpammer.blocks_name.append(block[0])
        if not AdminStateSpammer.blocks_name:
            await message.answer("Блоки не были добавлены", reply_markup=start_kb())
            return
        await message.answer("Выберите блок", reply_markup=block_pool_kb(AdminStateSpammer.blocks_name))
        await state.set_state(AdminStateSpammer.choose_block)

    except Exception as e:
        await message.answer('Ошибка при попытке подключения к базе данных', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return


@admin_manage_sender_router.message(StateFilter(AdminStateSpammer), F.text == 'Отправить спам')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    await message.answer("Напишите тест для рассылки всем пользователям",
                         reply_markup=back_kb())
    await state.set_state(AdminStateSpammer.set_text_spam)


@admin_manage_sender_router.message(AdminStateSpammer.set_text_spam, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        await message.answer("Начало рассылки")
        users = await get_all_users_id(session)
        for user in users:
            await message.bot.send_message(chat_id=user._data[0], text=message.text)
        await message.answer("Рассылка завершена", reply_markup=start_kb())

    except Exception as e:
        await message.answer('Ошибка при попытке подключения к базе данных', reply_markup=start_kb())
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
        await message.answer('Ошибка при попытке подключения к базе данных', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return


@admin_manage_sender_router.message(StateFilter(AdminStateSpammer), F.text == 'Выслать вебинар')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminStateSpammer.discription_vebinar = None
    await message.answer("Введите описание рассылки", reply_markup=back_kb())
    await state.set_state(AdminStateSpammer.set_text_vebinar)




@admin_manage_sender_router.message(AdminStateSpammer.set_text_vebinar, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminStateSpammer.discription_vebinar = message.text
    await message.answer("Отправьте ссылку на вебинар", reply_markup=back_kb())
    await state.set_state(AdminStateSpammer.send_vebinar)


@admin_manage_sender_router.message(AdminStateSpammer.send_vebinar, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminStateSpammer.web_vebinar = message.text
    count_send = 0
    try:
        await message.answer("Начало рассылки")
        next_block_progress = await get_next_block_progress(session)
        users = await get_all_users_id_progress(session)
        for user in users:
            if user[1] == next_block_progress[0]:
                count_send += 1
                await message.bot.send_message(chat_id=user._data[0], text=AdminStateSpammer.discription_vebinar,
                                               reply_markup=get_inline_vebinar(url=AdminStateSpammer.web_vebinar))
        await message.answer(f"Успешная рассылка. Выслано {count_send} пользователям", reply_markup=spam_actions_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
    except Exception as e:
        await message.answer('Ошибка при попытке подключения к базе данных', reply_markup=start_kb())
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
    if not date:
        date = datetime.datetime.now()
        selected = True
    date = date.replace(hour=10, minute=0)
    if selected:
        await callback_query.message.answer(
            f'Вы выбрали {date.strftime("%d.%m.%Y")}',
            reply_markup=start_kb()
        )
    try:
        await set_date_post_block_by_name(session, block_name=AdminStateSpammer.name_of_block,
                                          date_to_post=date)
        await callback_query.message.answer('Изменение успешно применено', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)

    except Exception as e:
        await callback_query.message.answer('Ошибка при попытке подключения к базе данных', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return
