import logging

import emoji
from aiogram.filters import Command, or_f, StateFilter, CommandStart
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import check_new_user, add_user
from handlers.user.user_callback_router import user_callback_router
from keyboards.user.inline_user import get_inline
from keyboards.user.reply_user import start_kb

user_private_router = Router()
user_private_router.include_routers(user_callback_router)


class UserState(StatesGroup):
    start_user = State()
    payment_user = State()
    user_task = State()
    data = {
        'subj': None,
        'module': None,
        'under_prepare': [],
        'under_prepare_choose': None,
        'prepare': None,
    }


@user_private_router.message(StateFilter('*'), CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        userid, username = message.from_user.id, message.from_user.full_name
        res = await check_new_user(session, userid)
        if len(res) == 0:
            await add_user(session, userid, username)
    except Exception as e:
        logging.info(e)
        await message.answer('Ошибка регистрации', reply_markup=start_kb())
    text = f'Привет {message.from_user.full_name}'
    await message.answer(text, reply_markup=start_kb())
    await message.answer('Готовим блок для тебя ...')
    await state.set_state(UserState.start_user)

