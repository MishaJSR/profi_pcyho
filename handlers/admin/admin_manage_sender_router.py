import datetime

from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_block import get_block_active, get_block_names_all, get_date_post_block_by_name, \
    set_date_post_block_by_name
from database.orm_query_task import get_task_by_block_id
from keyboards.admin.reply_admin import start_kb, spam_actions_kb, block_pool_kb, back_kb
from handlers.admin.states import AdminStateSpammer

admin_manage_sender_router = Router()


@admin_manage_sender_router.message(StateFilter(AdminStateSpammer), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    print(current_state)

    if current_state == AdminStateSpammer.choose_block or current_state == AdminStateSpammer.start:
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
        await message.answer(text='Выберите блок',
                             reply_markup=block_pool_kb(AdminStateSpammer.blocks_name))
        await state.set_state(AdminStateSpammer.choose_block)
        return


@admin_manage_sender_router.message(F.text == 'Рассылка')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer('Выберите действие', reply_markup=spam_actions_kb())
    await state.set_state(AdminStateSpammer.spam_actions)


@admin_manage_sender_router.message(AdminStateSpammer.spam_actions, F.text == 'Отобразить статус блоков')
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
        await state.set_state(AdminStateSpammer.start)
        return


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


@admin_manage_sender_router.message(AdminStateSpammer.choose_block, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        AdminStateSpammer.name_of_block = message.text
        date_post = await get_date_post_block_by_name(session, block_name=AdminStateSpammer.name_of_block)
        date_post = date_post[0].strftime("%d.%m.%Y %H:%M")
        await message.answer(f'Прошлая дата публикации блока {AdminStateSpammer.name_of_block[:-6]}\n'
                             f'{date_post[:-6]}\nВведите новую дату в формате 10.02.2024',
                             reply_markup=back_kb())
        await state.set_state(AdminStateSpammer.confirm_date)

    except Exception as e:
        await message.answer('Ошибка при попытке подключения к базе данных', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return


@admin_manage_sender_router.message(AdminStateSpammer.confirm_date, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        d, m, y = message.text.split('.')
        h, minute = 10, 00
        date_to_post = datetime.datetime(year=int(y), month=int(m), day=int(d), hour=int(h), minute=int(minute))
        await set_date_post_block_by_name(session, block_name=AdminStateSpammer.name_of_block,
                                          date_to_post=date_to_post)
        await message.answer('Изменение успешно применено', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)

    except Exception as e:
        await message.answer('Ошибка при попытке подключения к базе данных', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return
