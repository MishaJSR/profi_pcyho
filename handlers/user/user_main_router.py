import datetime
import logging
import pywhatkit

from aiogram.filters import Command, StateFilter, CommandStart
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_user import check_new_user, add_user
from database.orm_query_block import get_time_next_block
from database.orm_query_user import get_progress_by_user_id, get_user_points
from handlers.user.user_callback_router import user_callback_router
from handlers.user.user_states import UserRegistrationState
from keyboards.admin.inline_admin import get_inline_parent
from keyboards.user.reply_user import start_kb, send_contact_kb, users_pool_kb, users_pool, parent_permission

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
    if len(message.text) > 6:
        UserRegistrationState.children_id = message.text.split(' ')[1]
        await message.answer("тут должно быть превью курса")
        await message.answer("Разрешить вашему ребёнку пройти наш курс?", reply_markup=parent_permission())
        return
    await message.answer(f'Привет {message.from_user.full_name}')
    await message.answer(text="Укажи кем ты являешься", reply_markup=users_pool_kb())
    await state.set_state(UserRegistrationState.start)
    # try:
    #     userid, username = message.from_user.id, message.from_user.full_name
    #     res = await check_new_user(session, userid)
    #     if len(res) == 0:
    #         await add_user(session, userid, username)
    #         await message.answer(f'Привет {message.from_user.full_name}')
    #         await message.answer('Готовим урок для тебя ...')
    #         return
    #     await message.answer(f'Привет {message.from_user.full_name}', reply_markup=start_kb())
    # except Exception as e:
    #     logging.info(e)
    #     await message.answer('Ошибка регистрации')
    # await state.set_state(UserState.start_user)

@user_private_router.message(StateFilter('*'), F.text == "Да, я даю согласие")
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    await message.answer("Спасибо Вам за доверие", reply_markup=ReplyKeyboardRemove())
    await message.answer("Хочу тоже попробовать курс!", reply_markup=get_inline_parent())


@user_private_router.message(StateFilter('*'), F.text == "Нет, я против")
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    await message.answer("Нам очень жаль, напишите что вам не понравилось", reply_markup=ReplyKeyboardRemove())
    await message.answer("Возможно вы сами хотите попробовать пройти курс?", reply_markup=get_inline_parent())


@user_private_router.message(UserRegistrationState.start, F.text)
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text not in users_pool:
        await message.answer(f'Я не распознала твоего ответа\nПопробуй снова')
        return
    try:
        await add_user(session, user_id=message.from_user.id,
                       username=message.from_user.full_name,
                       user_class=message.text)
        if message.text == "Ребёнок":
            link = f"https://t.me/train_chiildren_psychology_bot?start={message.from_user.id}"
            await message.answer(f"Для продолжения обучения необходимо разрешение родителя\n"
                                 f"Если он согласится на твое обучение, Хэппи отправит тебе твой первый урок")
            await message.answer(link)
            await message.answer("Отправь эту ссылку своему родителю")
            await state.set_state(UserRegistrationState.children)
        elif message.text == "Родитель":
            await state.set_state(UserRegistrationState.parent)
        else:
            await state.set_state(UserRegistrationState.teacher)
    except Exception as e:
        await message.answer("Ошибка регистрации")


@user_private_router.message(UserRegistrationState.children)
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    if not message.contact:
        await message.answer(f"Не поняла твоего сообщения\nЧтобы отправить контакт родителя:\n"
                             "1. Открой его профиль в телеграмм\n"
                             "2. Нажми на кнопку Поделиться контактом\n"
                             "3. Отправь контакт Хэппи")
        return
    user_id = message.contact.user_id
    await message.bot.send_message(chat_id=user_id, text="Привет Петушок")


@user_private_router.message(StateFilter('*'), F.contact)
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    pywhatkit.sendwhatmsg('+79111938665', 'Привет мир!', 12, 35)
    # user_id = message.contact.user_id
    # await message.bot.send_message(chat_id=user_id, text="Привет Хетаг")


@user_private_router.message(StateFilter('*'), Command("points"))
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    points = await get_user_points(session, user_id=message.from_user.id)
    await message.answer(f'У Вас на счету: {points[0]} очков')


@user_private_router.message(StateFilter('*'), F.text == 'Когда будет следующий блок?')
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_progress_by_user_id(session, user_id=message.from_user.id)
        res2 = await get_time_next_block(session, progress_block=res[0])
        if res2[0] < datetime.datetime.now():
            await message.answer(f"Следующий урок уже вышел\n"
                                 f"Если вы уже прошли все задания, Хэппи в ближайшее время вышлет Вам новый урок",
                                 reply_markup=ReplyKeyboardRemove())
        else:
            rus_date = res2[0].strftime("%d.%m.%Y %H:%M")
            await message.answer(f"Следующий урок выйдет {rus_date}")
    except Exception as e:
        await message.answer(f"Обучение пройдено, спасибо что были с нами!!!")


