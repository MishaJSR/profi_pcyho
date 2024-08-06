import asyncio

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InputMediaPhoto, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_block.orm_query_block import get_block_id_by_callback, get_block_id_by_progress
from database.orm_task.orm_query_task_media import get_media_task_by_task_id
from database.orm_task.orm_query_task import get_task_by_block_id
from database.orm_user.orm_query_user import update_user_progress, update_user_points, get_user_class, \
    get_progress_by_user_id, \
    update_user_become, add_user, check_user_subscribe_new_user, \
    check_user_become_children, get_user_progress, get_user_points, get_parent_by_id, \
    get_user_class_session, get_parent_by_ses, update_users_progress_session
from database.orm_user.orm_query_user_task_progress import set_user_task_progress, get_task_progress_by_user_id, \
    get_is_pass_by_id, delete_all_user_progress
from handlers.user.state import UserState
from handlers.user.user_states import UserRegistrationState
from keyboards.admin.inline_admin import get_inline_parent_all_block, get_inline_is_like, \
    get_inline_pay, get_inline_parent_all_block_pay, get_inline_teacher_all_block_referal, get_inline_next_block, \
    questions_kb, get_inline_pay_end, skip_task_kb, get_inline_support, get_inline_to_tasks, get_inline_next_test_good, \
    get_inline_next_test_bad, get_third_block2, get_third_block3, get_inline_is_like_end, get_inline_mind
from keyboards.user.reply_user import send_contact_kb
from utils.common.message_constant import pay_to_link, you_should_be_partner, congratulations, \
    get_phone, message_first_block, message_second_block, list_number_smile, file_id, text_for_media, \
    question_answer, message_third_block, achive3, photo_media11, photo_media12, photo_media13, photo_media14, \
    photo_media21, photo_media22, photo_media23, photo_media24, photo_media25, photo3, photo4
from utils.spam_def.spam_send import spam_task_user

user_callback_router = Router()


class UserCallbackState(StatesGroup):
    start_callback = State()
    image_callback = State()
    test_callback = State()
    user_callback = State()
    tasks = []
    count_tasks = None
    block_id = None
    now_task = None
    list_of_answers = []
    callback_data = None
    is_return = False
    index = 1


@user_callback_router.callback_query(lambda call: call.data == "get_third_block1")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Навыки эмоционального интеллекта оценены?", reply_markup=get_third_block2())
    await call.answer("Хорошо, идем дальше")


@user_callback_router.callback_query(lambda call: call.data == "get_third_block2")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Ситуации, в которых тебе пригодится высокий скилл эмоционального интеллекта, придуманы?",
                              reply_markup=get_third_block3())
    await call.answer("Хорошо, идем дальше")


@user_callback_router.callback_query(lambda call: call.data == "get_third_block3")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    user_id = call.from_user.id
    user_class = await get_user_class_session(session, user_id=user_id)
    if user_class[0] == "Ребёнок":
        await call.message.answer_photo(photo=achive3, caption=congratulations, reply_markup=ReplyKeyboardRemove())
        await call.message.answer(text=question_answer)
        parents = await get_parent_by_ses(session, user_id=user_id)
        for parent in parents:
            mom_id = parent[0]
            try:
                await call.message.bot.send_message(chat_id=mom_id,
                                                    text=message_third_block,
                                                    reply_markup=get_inline_pay_end())
                await asyncio.sleep(3)
                media1 = [InputMediaPhoto(type='photo', media=photo_media11),
                         InputMediaPhoto(type='photo', media=photo_media12),
                         InputMediaPhoto(type='photo', media=photo_media13),
                         InputMediaPhoto(type='photo', media=photo_media14)]
                media2 = [InputMediaPhoto(type='photo', media=photo_media21),
                         InputMediaPhoto(type='photo', media=photo_media22),
                         InputMediaPhoto(type='photo', media=photo_media23),
                         InputMediaPhoto(type='photo', media=photo_media24),
                         InputMediaPhoto(type='photo', media=photo_media25)]
                await call.message.bot.send_media_group(chat_id=mom_id, media=media1)
                await call.message.bot.send_message(chat_id=mom_id, text="Представили?",
                                                    reply_markup=get_inline_mind())
                await asyncio.sleep(4)
                await call.message.bot.send_media_group(chat_id=mom_id, media=media2)
                await call.message.bot.send_message(chat_id=mom_id, text="Как Вам?",
                                                    reply_markup=get_inline_is_like_end())
                await asyncio.sleep(4)
                await call.message.bot.send_photo(chat_id=mom_id, photo=photo3,)
                await call.message.bot.send_message(chat_id=mom_id, text="Как Вам?",
                                                    reply_markup=get_inline_is_like_end())
                await asyncio.sleep(5)
                await call.message.bot.send_photo(chat_id=mom_id, photo=photo4,
                                                  reply_markup=get_inline_parent_all_block_pay())
            except Exception as e:
                pass
    elif user_class[0] == "Родитель":
        await call.message.answer_photo(photo=achive3,
                                  caption=f"Поздравляю!\n"
                                  f"Первая глава квеста завершена🔥\n"
                                  f"Вы также можете забронировать полный курс по ссылке",
                                  reply_markup=get_inline_parent_all_block_pay())
        await call.message.answer(text=question_answer)
    else:
        await call.message.answer_photo(photo=achive3,
                                        caption=f"Поздравляю!\n"
                                       f"Первая глава квеста завершена🔥\n"
                                       f"{you_should_be_partner}",
                                  reply_markup=get_inline_teacher_all_block_referal())
        await call.message.answer(text=question_answer)
    await update_users_progress_session(session, user_id=user_id)


@user_callback_router.callback_query(lambda call: call.data == "parent_want_to_be_children")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    await update_user_become(session, user_id=call.from_user.id)
    await update_user_progress(session, user_id=call.from_user.id)
    await call.answer("Хорошо, идем дальше")
    await call.message.answer("Хорошо👍 \nИдем дальше 💪")
    await asyncio.sleep(3)
    await spam_task_user(call.message.bot, session, call.from_user.id)


@user_callback_router.callback_query(lambda call: call.data == "pay")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Ссылка на оплату", reply_markup=get_inline_pay())


@user_callback_router.callback_query(lambda call: call.data == "referal_teacher")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    await call.message.answer("Ссылка на оплату", reply_markup=get_inline_pay())


@user_callback_router.callback_query(lambda call: call.data == "back_from_pay")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    is_become = await check_user_become_children(session, user_id=call.from_user.id)
    if is_become[0]:
        await call.message.answer(pay_to_link,
                                  reply_markup=get_inline_parent_all_block_pay())
    else:
        await call.message.answer(pay_to_link,
                                  reply_markup=get_inline_parent_all_block())


@user_callback_router.callback_query(lambda call: call.data == "parent_registration")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    try:
        is_sub, user_class, user_callback, phone_number, name_of_user = await check_user_subscribe_new_user(session,
                                                                                                            user_id=call.from_user.id)
        await call.message.answer("Вы уже зарегистрированы")
    except Exception as e:
        await add_user(session, user_id=call.from_user.id,
                       username=call.from_user.full_name,
                       user_tag=call.from_user.username,
                       user_class="Родитель")
        await call.message.answer(get_phone, reply_markup=send_contact_kb())
        await call.answer("Начало регистрации")
        await state.set_state(UserRegistrationState.parent)


#
@user_callback_router.callback_query(lambda call: call.data == "back_to_theory")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()


@user_callback_router.callback_query(lambda call: len(call.data) == 36)
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    await call.message.answer_photo(photo=file_id, caption=text_for_media, reply_markup=get_inline_to_tasks(),
                                    parse_mode="HTML")
    UserCallbackState.callback_data = call.data


@user_callback_router.callback_query(lambda call: "start_task" in call.data)
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    UserCallbackState.is_return = False
    if "return" in call.data:
        UserCallbackState.is_return = True
        await delete_all_user_progress(session, user_id=call.from_user.id)

    UserCallbackState.tasks = []
    UserCallbackState.block_id = None
    UserCallbackState.now_task = None
    callback_data = UserCallbackState.callback_data
    UserCallbackState.block_id = await get_block_id_by_callback(session, callback_button_id=callback_data)
    tasks = await get_task_by_block_id(session, block_id=UserCallbackState.block_id[0])
    ready_tasks = await get_task_progress_by_user_id(session, user_id=call.from_user.id,
                                                     block_id=UserCallbackState.block_id[0])
    if not tasks:
        await call.message.answer("Заданий по этому блоку нет")
        await call.answer('Вы выбрали задание')
        return
    if len(ready_tasks) >= len(tasks):
        await call.message.answer("Задания уже были пройдены")
        await call.answer('Вы выбрали задание')
        return
    if ready_tasks:
        tasks = tasks[len(ready_tasks):]
    for task in tasks:
        UserCallbackState.tasks.append(task._data[0])
    if not UserCallbackState.tasks:
        await call.message.answer("Задания отсутствуют")
        await call.answer('Вы выбрали задание')
        return
    UserCallbackState.now_task = UserCallbackState.tasks[0]
    UserCallbackState.tasks = UserCallbackState.tasks[1:]
    await prepare_test_tasks(call.message, state, session)
    await call.answer('Вы выбрали задание')


@user_callback_router.callback_query(lambda call: call.data == "next_block_children")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    user_class, user_become = await get_user_class(session, user_id=call.from_user.id)
    if user_class != "Ребёнок" and not user_become:
        await call.message.answer('Вам понравилось?', reply_markup=get_inline_is_like())
        await call.answer("Вам понравилось?")
        return
    await update_user_progress(session, user_id=call.from_user.id)
    await spam_task_user(call.message.bot, session, call.from_user.id)
    await call.answer("Идем дальше")


@user_callback_router.callback_query(lambda call: call.data == "go_to_quest")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    if not UserCallbackState.is_return:
        await update_user_progress(session, user_id=call.from_user.id)
        await spam_task_user(call.message.bot, session, call.from_user.id)
    else:
        UserCallbackState.is_return = False
    await call.answer("Идем дальше")


@user_callback_router.message(UserCallbackState.test_callback, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Повторите попытку. Ответы должны быть в формате 134")
        return
    try:
        answer_user = sorted([int(ans) for ans in message.text])
    except ValueError as e:
        await message.answer("Повторите попытку. Ответы должны быть в формате 134")
        return
    answer_right = sorted([int(ans) for ans in UserCallbackState.now_task.answer])
    is_pass = False
    if answer_user == answer_right:
        is_pass = True
    await state.set_state(UserState.start_user)
    if is_pass:
        await message.answer("Верно! Идем дальше?", reply_markup=get_inline_next_test_good())
    else:
        await message.answer("Неверно. Ты сможешь вернутся к этому заданию позже. Готов к новому вопросу?",
                             reply_markup=get_inline_next_test_bad())
    await set_user_task_progress(session, user_id=message.from_user.id, task_id=UserCallbackState.now_task.id,
                                 username=message.from_user.full_name, block_id=UserCallbackState.now_task.block_id,
                                 answer_mode=UserCallbackState.now_task.answer_mode, result=message.text,
                                 is_pass=is_pass)
    # await update_user_task_progress_and_go_to_next(message, session, state, is_pass)


@user_callback_router.callback_query(lambda call: call.data == "next_test_good")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    if len(UserCallbackState.tasks) != 0:
        UserCallbackState.now_task = UserCallbackState.tasks[0]
        UserCallbackState.index += 1
        UserCallbackState.tasks = UserCallbackState.tasks[1:]
        await prepare_test_tasks(call.message, state, session)
    else:
        await update_user_task_progress_and_go_to_next(call, call.message, session)


@user_callback_router.callback_query(lambda call: call.data == "next_test_bad")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    await call.answer("Идем дальше")
    if len(UserCallbackState.tasks) != 0:
        UserCallbackState.now_task = UserCallbackState.tasks[0]
        UserCallbackState.index += 1
        UserCallbackState.tasks = UserCallbackState.tasks[1:]
        await prepare_test_tasks(call.message, state, session)
    else:
        await update_user_task_progress_and_go_to_next(call, call.message, session)


async def update_user_task_progress_and_go_to_next(call, message, session):
    UserCallbackState.index = 1
    progress = await get_user_progress(session, user_id=call.from_user.id)
    await call.answer(f"Задания пройдены")
    user_class, user_become = await get_user_class(session, user_id=call.from_user.id)
    res = await get_is_pass_by_id(session, block_id=UserCallbackState.now_task.block_id,
                                  user_id=call.from_user.id)
    return_callback = "start_task" + "return"
    callback = 'next_block_children'
    is_pass = 0
    for el in res:
        if not el[0]:
            is_pass += 1
    if is_pass == 0:
        await update_user_points(session, user_id=call.from_user.id, points=100)
    points = await get_user_points(session, user_id=call.from_user.id)
    if is_pass == 0 and UserCallbackState.is_return:
        await message.answer(f"Эпизод №{progress[0]} пройден ✅")
        await message.answer(text=f"Поздравляю! На твоем счету {points[0]} е-коинов💰\n"
                                                        f"Это твоя награда за упорство💪\n"
                                                        f"Двигайся дальше и получай новые награды🏆\n"
                                                        f"Узнай для чего они нужны \nвот тут 👉 "
                                                        f"/coins_avail"
                                   )

    if is_pass == 0 and not UserCallbackState.is_return:
        await message.answer(f"Эпизод №{progress[0]} пройден ✅")
        await message.answer(text=f"Поздравляю 👏\n"
                                                        f"Поздравляю! На твоем счету {points[0]} е-коинов💰\n"
                                                        f"Двигайся дальше и получай новые награды.\n"
                                                        f"Узнай для чего они нужны вот тут 👉 "
                                                        f"/coins_avail")
    if is_pass != 0:
        await message.answer("Хочешь пройти испытания повторно и получить награду?  💰",
                             reply_markup=skip_task_kb(return_callback, callback))
    if is_pass == 0:
        if user_class != "Ребёнок" and not user_become:
            await message.answer('Вам понравилось?', reply_markup=get_inline_is_like())
        elif user_class != "Ребёнок" and not user_become:
            await message.answer('Перейдем к следующему эпизоду? 🤩', reply_markup=get_inline_next_block())
        else:
            await message.answer('Перейдем к следующему эпизоду? 🤩', reply_markup=get_inline_next_block())
    progress = await get_progress_by_user_id(session, user_id=call.from_user.id)
    res = await get_block_id_by_progress(session, progress_block=progress[0])
    if not res:
        if user_become and user_class == "Родитель":
            await message.answer(congratulations, reply_markup=ReplyKeyboardRemove())
            await message.answer(pay_to_link, reply_markup=get_inline_parent_all_block_pay())
            await message.answer(f'У вас остались вопросы ❓', reply_markup=questions_kb())
            return
        if user_class == "Педагог":
            await message.answer(congratulations, reply_markup=ReplyKeyboardRemove())
            await message.answer(you_should_be_partner, reply_markup=get_inline_teacher_all_block_referal())
            await message.answer(f'У вас остались вопросы ❓', reply_markup=questions_kb())
            return
        await message.answer(congratulations, reply_markup=ReplyKeyboardRemove())
    else:
        if user_class == "Ребёнок" and not UserCallbackState.is_return:
            parents = await get_parent_by_id(session, user_id=call.from_user.id)
            for parent in parents:
                mom_id = parent[0]
                child_progress = parent[1]
                try:
                    if child_progress == 1:
                        await message.bot.send_message(chat_id=mom_id,
                                                       text=message_first_block)
                    if child_progress == 2:
                        await message.bot.send_message(chat_id=mom_id,
                                                       text=message_second_block,
                                                       reply_markup=get_inline_support())
                except Exception as e:
                    pass
            return
    return


# dfsdf
async def prepare_test_tasks(message, state, session):
    media_group = []
    answers = UserCallbackState.now_task.answers.replace("\n", "\n\n")
    caption_text = list_number_smile[
                       UserCallbackState.index - 1] + " " + UserCallbackState.now_task.description + "\n\n" + answers + \
                   '\n\n' + UserCallbackState.now_task.addition
    photos = await get_media_task_by_task_id(session, task_id=UserCallbackState.now_task.id)
    if len(photos) > 0:
        for index, photo in enumerate(photos):
            if not index:
                media_group.append(
                    InputMediaPhoto(type='photo', media=photo[0], caption=caption_text, parse_mode="Markdown"))
            else:
                media_group.append(InputMediaPhoto(type='photo', media=photo[0]))
        await message.answer_media_group(media_group, reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(caption_text, parse_mode="Markdown")
    await state.set_state(UserCallbackState.test_callback)


async def prepare_image_task(message, state, session):
    media_group = []
    photos = await get_media_task_by_task_id(session, task_id=UserCallbackState.now_task.id)
    for index, photo in enumerate(photos):
        media_group.append(InputMediaPhoto(type='photo', media=photo[0]))
    await message.answer_media_group(media=media_group)
    await message.answer(f"{UserCallbackState.now_task.description}", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserCallbackState.image_callback)


def is_part_in_list(str_, words):
    for word in words:
        if word.lower() in str_.lower():
            return True
    return False
