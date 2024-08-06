import datetime
import logging

import emoji
from aiogram.filters import Command, StateFilter, CommandStart, ChatMemberUpdatedFilter, KICKED
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_user.orm_query_user import check_new_user, add_user, update_parent_id, get_user_parent, \
    update_user_phone, \
    update_user_subscribe, check_user_subscribe, update_user_callback, get_user_class, \
    update_user_block_bot_session_pool
from database.orm_block.orm_query_block import get_time_next_block
from database.orm_user.orm_query_user import get_progress_by_user_id, get_user_points
from handlers.user.user_callback_router import user_callback_router
from handlers.user.user_states import UserRegistrationState
from keyboards.admin.inline_admin import get_inline_parent, get_inline_parent_all_block, get_inline_is_like, \
    get_inline_parent_all_block_pay, get_inline_teacher_all_block, get_inline_teacher_all_block_referal, questions_kb, \
    get_inline_first_video
from keyboards.user.reply_user import send_contact_kb, users_pool_kb, users_pool, parent_permission
from utils.common.message_constant import pay_to_link, you_should_be_partner, congratulations, get_phone, \
    message_coints_avail, first_photo_id, happy_photo_id

user_private_router = Router()
user_private_router.include_routers(user_callback_router)


@user_private_router.message(StateFilter('*'), Command("coins"))
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        points = await get_user_points(session, user_id=message.from_user.id)
        await message.answer(f'У Вас на счету: {points[0]} e-коинов 💰')
        await message.answer(f"Узнай для чего они нужны "
                             f"/coins_avail")
    except Exception as e:
        await message.answer(f'У Вас на счету пока нет e-коинов 💰')
        await message.answer(f"Узнай для чего они нужны "
                             f"/coins_avail")


@user_private_router.message(StateFilter('*'), Command("coins_avail"))
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    await message.answer(f'{message_coints_avail}')


@user_private_router.message(StateFilter('*'), Command("questions"))
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    await message.answer(f'У вас остались вопросы ❓', reply_markup=questions_kb())


@user_private_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated, session: AsyncSession):
    try:
        await update_user_block_bot_session_pool(session, user_id=event.from_user.id)
    except Exception as e:
        pass


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
                await message.answer("Эта ссылка уже использована")
                return
            if UserRegistrationState.children_id == message.from_user.id:
                await message.answer("Эта ссылка для родителя")
                return
            await message.answer(f"Привет!\n\nВаш ребенок хочет улучшить навыки "
                                 f"живого общения и научиться управлять своими эмоциями в “Студии эмоций”\n\n"
                                 f"{message.from_user.full_name}, вы разрешаете "
                                 f"ребенку пройти бесплатный уровень "
                                 f"онлайн-квеста “Герой эмоций”?\n\n"
                                 f"Если вы пройдете регистрацию, "
                                 f"я пришлю вам результаты прохождения по каждому уроку."
                                 f"", reply_markup=parent_permission())
            return
    except Exception as e:
        await message.answer("Ошибка подключения")
        logging.info(e)


@user_private_router.message(StateFilter('*'), CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    res = await check_new_user(session, user_id=message.from_user.id)
    if not res:
        await message.answer_photo(photo=happy_photo_id, caption=f'{message.from_user.full_name}, '
                                                                 f'добро пожаловать на квест!\n\n'
                                                                 f'Я - робот-помощник, а ты?',
                                   reply_markup=users_pool_kb())
        await state.set_state(UserRegistrationState.start)
        return
    is_sub, progress, user_class, user_callback, user_become, name_of_user = await check_user_subscribe(session,
                                                                                                        user_id=message.from_user.id)
    if user_class == "Ребёнок":
        if not is_sub:
            await message.answer(f'Привет {message.from_user.full_name}!')
            await message.answer('Родитель еще не подтвердил доступ')
            return
        await message.answer(f'Привет {message.from_user.full_name}!')
        await message.answer('Урок уже выслан\n'
                             'Пожалуйста ознакомьтесь с ним и пройдите задания')
        return
    if not is_sub:
        await message.answer(get_phone, reply_markup=send_contact_kb())
        await state.set_state(UserRegistrationState.parent)
        return
    # if not user_callback and not user_become:
    #     await message.answer('Вам понравилось?', reply_markup=get_inline_is_like())
    #     return
    if progress < 3 and user_class == "Педагог":
        await message.answer('Урок уже выслан\n'
                             'Пожалуйста ознакомьтесь с ним и пройдите задания')
        return
    if progress < 3 and user_class == "Родитель":
        await message.answer('Урок уже выслан\n'
                             'Пожалуйста ознакомьтесь с ним и пройдите задания')
        return
    # if user_class == "Родитель" and not user_become:
    #     await message.answer("Хочу пройти все блоки", reply_markup=get_inline_parent_all_block())
    #     return
    # if user_class == "Педагог" and not user_become:
    #     await message.answer("Вы также можете стать нашим партнером", reply_markup=get_inline_teacher_all_block())
    #     return
    if user_class == "Педагог" and user_become:
        await message.answer(you_should_be_partner, reply_markup=get_inline_teacher_all_block_referal())
        return
    if user_class == "Родитель" and user_become:
        await message.answer(pay_to_link, reply_markup=get_inline_parent_all_block_pay())
        return


@user_callback_router.callback_query(lambda call: call.data in ["yes", "no", "skip"])
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    data = str(call.data)
    await call.message.delete()
    await update_user_callback(session, user_id=call.from_user.id, user_callback=data)
    await call.answer("Спасибо за ответ!")
    await call.message.answer("Спасибо за ответ!\n"
                              "Ваше мнение очень важно для нас " + emoji.emojize('🤗'), reply_markup=ReplyKeyboardRemove())
    user_class = await get_user_class(session, user_id=call.from_user.id)
    if user_class[0] == "Педагог":
        await call.message.answer(you_should_be_partner,
                                  reply_markup=get_inline_teacher_all_block())
    else:
        await call.message.answer(pay_to_link,
                                  reply_markup=get_inline_parent_all_block())


@user_private_router.message(StateFilter('*'), F.text == "Да, я даю согласие")
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    try:

        progress_children = await get_progress_by_user_id(session, user_id=UserRegistrationState.children_id)
        if progress_children[0] != 0:
            await message.answer("Вы уже дали согласие")
            return
        await update_parent_id(session, user_id=UserRegistrationState.children_id, parent_id=message.from_user.id)
        await message.answer("Спасибо Вам за доверие", reply_markup=ReplyKeyboardRemove())
        await message.bot.send_photo(chat_id=UserRegistrationState.children_id, photo=first_photo_id,
                                     caption=f"Ура, доступ разблокирован!\n\n"
                                             f"На связи Хэппи 😊 и я рада приветствовать тебя на интерактивном квесте “Герой эмоций”! 🎉\n",
                                     reply_markup=ReplyKeyboardRemove())
        await message.bot.send_message(chat_id=UserRegistrationState.children_id, text="Ты готов отправиться со мной ?",
                                       reply_markup=get_inline_first_video())
        res = await check_new_user(session, user_id=message.from_user.id)
        if not res:
            await message.answer("Хочу тоже попробовать курс!", reply_markup=get_inline_parent())
    except Exception as e:
        logging.info(e)
        await message.answer("Ошибка подключения")


@user_private_router.message(StateFilter('*'), F.text == "Нет, я против")
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    await message.answer("Нам очень жаль 😔", reply_markup=ReplyKeyboardRemove())
    res = await check_new_user(session, user_id=message.from_user.id)
    if not res:
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
                f"Поздравляю!\nТы прошел начальный уровень квеста!\n", reply_markup=ReplyKeyboardRemove())
            await message.answer(pay_to_link,
                                 reply_markup=get_inline_parent_all_block_pay())
            await message.answer("Остались вопросы? Используй команду /questions")
            return
        if user_class == "Педагог":
            await message.answer(
                f"Поздравляю!\nТы прошел начальный уровень квеста!\n", reply_markup=ReplyKeyboardRemove())
            await message.answer(you_should_be_partner, reply_markup=get_inline_teacher_all_block_referal())
            await message.answer("Остались вопросы? Используй команду /questions")
            return
        else:
            await message.answer(congratulations, reply_markup=ReplyKeyboardRemove())


@user_private_router.message(UserRegistrationState.start, F.text)
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.text not in users_pool:
        await message.answer(f'Я не распознала твоего ответа\nПопробуй снова')
        return
    try:
        if message.text == "Ребёнок":
            await add_user(session, user_id=message.from_user.id,
                           username=message.from_user.full_name,
                           user_tag=message.from_user.username,
                           user_class=message.text)
            link = f"https://t.me/train_chiildren_psychology_bot?start={message.from_user.id}"
            await message.answer(f"Для прохождения квеста мне необходимо получить разрешение от твоего родителя ✨\n"
                                 f"Когда он согласится, я пришлю тебе первое задание 🤓",
                                 reply_markup=ReplyKeyboardRemove())
            await message.answer("Отправь эту ссылку родителю 👇")
            await message.answer(link)
            await state.set_state(UserRegistrationState.children)
        elif message.text == "Родитель":
            await add_user(session, user_id=message.from_user.id,
                           username=message.from_user.full_name,
                           user_tag=message.from_user.username,
                           user_class=message.text)
            await message.answer(get_phone, reply_markup=send_contact_kb())
            await state.set_state(UserRegistrationState.parent)
        else:
            await add_user(session, user_id=message.from_user.id,
                           username=message.from_user.full_name,
                           user_tag=message.from_user.username,
                           user_class=message.text)
            await message.answer(get_phone, reply_markup=send_contact_kb())
            await state.set_state(UserRegistrationState.parent)
    except Exception as e:
        logging.info(e)
        await message.answer("Ошибка регистрации")


@user_private_router.message(UserRegistrationState.parent)
async def start_cmd(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.contact:
        phone_number = "+" + message.contact.phone_number
        await update_user_phone(session, phone_number=phone_number, user_id=message.from_user.id)
        await update_user_subscribe(session, user_id=message.from_user.id)
        await message.answer_photo(photo=first_photo_id,
                                   caption=f"На связи Хэппи 😊  и я рада приветствовать "
                                           f"тебя на интерактивном квесте “Герой эмоций”! 🎉\n",
                                   reply_markup=ReplyKeyboardRemove())
        await message.answer(text="Ты готов отправиться со мной ?", reply_markup=get_inline_first_video())
    if message.text == "Пропустить":
        await update_user_subscribe(session, user_id=message.from_user.id)
        await message.answer_photo(photo=first_photo_id,
                                   caption=f"На связи Хэппи 😊  и я рада приветствовать "
                                           f"тебя на интерактивном квесте “Герой эмоций”! 🎉\n",
                                   reply_markup=ReplyKeyboardRemove())
        await message.answer(text="Ты готов отправиться со мной ?", reply_markup=get_inline_first_video())
