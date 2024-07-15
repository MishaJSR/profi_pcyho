import datetime
import logging

import emoji
from aiogram.filters import Command, or_f, StateFilter, CommandStart
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import check_new_user, add_user
from database.orm_query_block import get_time_next_block
from database.orm_query_user import get_progress_by_user_id
from handlers.user.user_callback_router import user_callback_router
from keyboards.user.inline_user import get_inline
from keyboards.user.reply_user import start_kb, empty_kb

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
        text = f'Привет {message.from_user.full_name}'
        await message.answer(text)
        if len(res) == 0:
            await add_user(session, userid, username)
            await message.answer('Готовим блок для тебя ...')
    except Exception as e:
        logging.info(e)
        await message.answer('Ошибка регистрации')
    await state.set_state(UserState.start_user)


@user_private_router.message(StateFilter('*'), F.text == 'Когда будет следующий блок?')
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_progress_by_user_id(session, user_id=message.from_user.id)
        res2 = await get_time_next_block(session, progress_block=res[0])
        if res2[0] < datetime.datetime.now():
            await message.answer(f"Следующий блок уже вышел, для доступа пройдите задание\n", reply_markup=ReplyKeyboardRemove())
        else:
            rus_date = res2[0].strftime("%d.%m.%Y %H:%M")
            await message.answer(f"Следующий блок выйдет {rus_date}")
    except Exception as e:
        await message.answer(f"Обучение пройдено, спасибо что были с нами!!!")
