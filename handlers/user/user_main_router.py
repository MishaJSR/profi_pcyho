import datetime
import logging

from aiogram.filters import Command, StateFilter, CommandStart
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_user import check_new_user, add_user, update_parent_id, get_user_parent, update_user_phone, \
    update_user_subscribe, check_user_subscribe, update_user_callback, get_user_class
from database.orm_query_block import get_time_next_block
from database.orm_query_user import get_progress_by_user_id, get_user_points
from handlers.user.user_callback_router import user_callback_router
from handlers.user.user_states import UserRegistrationState
from keyboards.admin.inline_admin import get_inline_parent, get_inline_parent_all_block, get_inline_is_like, \
    get_inline_parent_all_block_pay
from keyboards.user.reply_user import start_kb, send_contact_kb, users_pool_kb, users_pool, parent_permission, \
    send_name_user_kb
from middlewares.throttling import throttled, ThrottlingMiddleware

user_private_router = Router()
user_private_router.include_routers(user_callback_router)


class UserState(StatesGroup):
    start_user = State()
    payment_user = State()
    user_task = State()
    user_callback = State()
    data = {
        'subj': None,
        'module': None,
        'under_prepare': [],
        'under_prepare_choose': None,
        'prepare': None,
    }


@user_private_router.message(StateFilter('*'), F.html_text.contains("/start "))
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        if len(message.text) > 6:
            UserRegistrationState.children_id = int(message.text.split(' ')[1])
            res_parent = await get_user_parent(session, user_id=UserRegistrationState.children_id)
            if not res_parent:
                await message.answer("Такого ребенка не найдено")
                return
            if res_parent[0]:
                await message.answer("Вы уже разрешили доступ ребенку")
                return
            if UserRegistrationState.children_id == message.from_user.id:
                await message.answer("Эта ссылка для родителя")
                return
            await message.answer("Разрешить вашему ребёнку пройти наш бесплатный курс?\n"
                                 "Вы будете получать его прогресс по урокам", reply_markup=parent_permission())
            return
    except Exception as e:
        await message.answer("Ошибка подключения")


@user_private_router.message(StateFilter('*'), CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    res = await check_new_user(session, user_id=message.from_user.id)
    if not res:
        await message.answer(f'Привет {message.from_user.full_name}')
        await message.answer(text="Укажи кем ты являешься", reply_markup=users_pool_kb())
        await state.set_state(UserRegistrationState.start)
        return
    is_sub, progress, user_class, user_callback, user_become, name_of_user = await check_user_subscribe(session,
                                                                                                        user_id=message.from_user.id)
    if user_class == "Ребёнок":
        await message.answer(f'С возвращением {message.from_user.full_name}', reply_markup=start_kb())
        await state.set_state(UserState.start_user)
        return
    if not is_sub:
        await message.answer("Мы будем очень рады, если вы оставите нам свой номер телефона",
                             reply_markup=send_contact_kb())
        await state.set_state(UserRegistrationState.parent)
        return
    if progress == 2 and user_class == "Педагог":
        await message.answer('Урок уже выслан\n'
                             'Пожалуйста ознакомьтесь с ним и пройдите задания')
        return
    if progress == 1 and user_class == "Родитель":
        await message.answer('Урок уже выслан\n'
                             'Пожалуйста ознакомьтесь с ним и пройдите задания')
        return
    if not user_callback and not user_become:
        await message.answer('Вам понравилось?', reply_markup=get_inline_is_like())
        return
    if user_class == "Родитель" and not user_become:
        await message.answer("Хочу пройти все блоки", reply_markup=get_inline_parent_all_block())
        return
    if user_class == "Педагог":
        await message.answer("ссылка для педагога")
        return
    if user_class == "Родитель" and user_become:
        await message.answer("Вы можете оплатить полный курс по ссылке", reply_markup=get_inline_parent_all_block_pay())
        return


@user_callback_router.callback_query(lambda call: call.data in ["yes", "no", "skip"])
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    data = str(call.data)
    await call.message.delete()
    await update_user_callback(session, user_id=call.from_user.id, user_callback=data)
    await call.answer("Спасибо за ответ!")
    await call.message.answer("Спасибо за ответ!", reply_markup=ReplyKeyboardRemove())
    user_class = await get_user_class(session, user_id=call.from_user.id)
    if user_class[0] == "Педагог":
        await call.message.answer("Ссылка для педагога")
    else:
        await call.message.answer("Вы можете оплатить полный курс по ссылке",
                                  reply_markup=get_inline_parent_all_block())


@user_private_router.message(StateFilter('*'), F.text == "Да, я даю согласие")
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    await update_parent_id(session, user_id=UserRegistrationState.children_id, parent_id=message.from_user.id)
    await message.answer("Спасибо Вам за доверие", reply_markup=ReplyKeyboardRemove())
    res = await check_new_user(session, user_id=message.from_user.id)
    if not res:
        await message.answer("Хочу тоже попробовать курс!", reply_markup=get_inline_parent())


@user_private_router.message(StateFilter('*'), F.text == "Нет, я против")
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    await message.answer("Нам очень жаль, напишите что вам не понравилось", reply_markup=ReplyKeyboardRemove())
    await message.answer("Возможно вы сами хотите попробовать пройти курс?", reply_markup=get_inline_parent())


@user_private_router.message(StateFilter('*'), F.text == 'Когда будет следующий блок?')
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        is_sub = await check_user_subscribe(session, user_id=message.from_user.id)
        if not is_sub[0]:
            await message.answer("Родитель еще не подтвердил твой доступ к блоку")
            return
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
        user_class, user_become = await get_user_class(session, user_id=message.from_user.id)
        if user_become:
            await message.answer(
                f"Поздравляю!\nТы прошел начальный уровень квеста!\n")
            await message.answer("Скрипт для родителя")
            await message.answer("Вы можете оплатить полный курс по ссылке",
                                 reply_markup=get_inline_parent_all_block_pay())
            return
        if user_class == "Педагог":
            await message.answer(
                f"Поздравляю!\nТы прошел начальный уровень квеста!\n")
            await message.answer("Скрипт для педагога")
            return
        else:
            await message.answer(
                f"Поздравляю!\nТы прошел начальный уровень квеста!\nПройди все уровни и стань героем эмоций")
            await message.answer("Скрипт для ребёнка")


@user_private_router.message(UserRegistrationState.start, F.text)
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text not in users_pool:
        await message.answer(f'Я не распознала твоего ответа\nПопробуй снова')
        return
    try:
        if message.text == "Ребёнок":
            await add_user(session, user_id=message.from_user.id,
                           username=message.from_user.full_name,
                           user_class=message.text)
            link = f"https://t.me/train_chiildren_psychology_bot?start={message.from_user.id}"
            await message.answer(f"Для продолжения обучения необходимо разрешение родителя\n"
                                 f"Если он согласится на твое обучение, Хэппи отправит тебе твой первый урок",
                                 reply_markup=ReplyKeyboardRemove())
            await message.answer("Отправь эту ссылку своему родителю")
            await message.answer(link)
            await state.set_state(UserRegistrationState.children)
        elif message.text == "Родитель":
            await add_user(session, user_id=message.from_user.id,
                           username=message.from_user.full_name,
                           user_class=message.text)
            await message.answer("Мы будем очень рады, если вы оставите нам свой номер телефона",
                                 reply_markup=send_contact_kb())
            await state.set_state(UserRegistrationState.parent)
        else:
            await add_user(session, user_id=message.from_user.id,
                           username=message.from_user.full_name,
                           user_class=message.text, progress=2)
            await message.answer("Мы будем очень рады, если вы оставите нам свой номер телефона",
                                 reply_markup=send_contact_kb())
            await state.set_state(UserRegistrationState.parent)
    except Exception as e:
        await message.answer("Ошибка регистрации")


@user_private_router.message(UserRegistrationState.parent)
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.contact:
        phone_number = "+" + message.contact.phone_number
        await update_user_phone(session, phone_number=phone_number, user_id=message.from_user.id)
    await update_user_subscribe(session, user_id=message.from_user.id)
    await message.answer("Представьте себя ребенком и погрузитесь полностью в прохождение онлайн-квеста",
                         reply_markup=ReplyKeyboardRemove())

    return


@user_private_router.message(StateFilter('*'), Command("points"))
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    points = await get_user_points(session, user_id=message.from_user.id)
    await message.answer(f'У Вас на счету: {points[0]} очков')
