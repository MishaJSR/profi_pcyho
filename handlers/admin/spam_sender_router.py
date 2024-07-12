from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import find_task, delete_task
from database.orm_query_block import get_block_active
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