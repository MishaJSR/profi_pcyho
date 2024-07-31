from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InputMediaPhoto, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_block.orm_query_block import get_block_id_by_callback, get_block_id_by_progress
from database.orm_task.orm_query_task_media import get_media_task_by_task_id
from database.orm_task.orm_query_task import get_task_by_block_id
from database.orm_user.orm_query_user import update_user_progress, update_user_points, get_user_class, get_progress_by_user_id, \
    update_user_become, add_user, check_user_subscribe_new_user, \
    check_user_become_children, get_user_progress, get_user_points
from database.orm_user.orm_query_user_task_progress import set_user_task_progress, get_task_progress_by_user_id
from handlers.user.state import UserState
from handlers.user.user_states import UserRegistrationState
from keyboards.admin.inline_admin import get_inline_parent_all_block, get_inline_is_like, \
    get_inline_pay, get_inline_parent_all_block_pay, get_inline_teacher_all_block_referal, get_inline_next_block
from keyboards.user.reply_user import start_kb, send_contact_kb
from utils.common.message_constant import pay_to_link, you_should_be_partner, congratulations, \
    get_phone

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


@user_callback_router.callback_query(lambda call: call.data == "parent_want_to_be_children")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    await update_user_become(session, user_id=call.from_user.id)
    await call.answer("Хорошо, идем дальше")
    await call.message.answer("Хорошо\nИдем дальше!")


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
                       user_class="Родитель")
        await call.message.answer(get_phone, reply_markup=send_contact_kb())
        await call.answer("Начало регистрации")
        await state.set_state(UserRegistrationState.parent)


@user_callback_router.callback_query(lambda call: call.data == "back_to_theory")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()


@user_callback_router.callback_query(lambda call: len(call.data) == 36)
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await call.message.delete()
    UserCallbackState.tasks = []
    UserCallbackState.block_id = None
    UserCallbackState.now_task = None
    UserCallbackState.callback_data = call.data
    callback_data = UserCallbackState.callback_data
    UserCallbackState.block_id = await get_block_id_by_callback(session, callback_button_id=callback_data)
    tasks = await get_task_by_block_id(session, block_id=UserCallbackState.block_id[0])
    ready_tasks = await get_task_progress_by_user_id(session, user_id=call.from_user.id,
                                                     block_id=UserCallbackState.block_id[0])
    if not tasks:
        await call.message.answer("Заданий по этому блоку нет", reply_markup=start_kb())
        await call.answer('Вы выбрали задание')
        return
    if len(ready_tasks) >= len(tasks):
        await call.message.answer("Задания уже были пройдены", reply_markup=start_kb())
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
    if UserCallbackState.now_task.answer_mode == 'Описание изображения':
        await prepare_image_task(call.message, state, session)
        await call.answer('Вы выбрали задание')
    else:
        await prepare_test_tasks(call.message, state, session)
        await call.answer('Вы выбрали задание')


@user_callback_router.callback_query(lambda call: call.data == "next_block_children")
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await update_user_progress(session, user_id=call.from_user.id)
    await call.answer("Идем дальше")
    await call.message.answer("Хэппи сейчас пришлет тебе новый урок")



# @user_callback_router.message(UserCallbackState.image_callback, F.text)
# async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
#     is_pass = is_part_in_list(message.text, UserCallbackState.now_task.answer.split(" "))
#     if is_pass:
#         await message.answer(f"Поздравляем !!!\nВы получили {UserCallbackState.now_task.points_for_task} очков")
#         await update_user_points(session, user_id=message.from_user.id,
#                                  points=UserCallbackState.now_task.points_for_task)
#     await update_user_task_progress_and_go_to_next(message, session, state, is_pass)


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
        await update_user_points(session, user_id=message.from_user.id,
                                 points=UserCallbackState.now_task.points_for_task)
    await state.set_state(UserState.start_user)
    await update_user_task_progress_and_go_to_next(message, session, state, is_pass)


async def update_user_task_progress_and_go_to_next(message, session, state, is_pass):
    await set_user_task_progress(session, user_id=message.from_user.id, task_id=UserCallbackState.now_task.id,
                                 username=message.from_user.full_name, block_id=UserCallbackState.now_task.block_id,
                                 answer_mode=UserCallbackState.now_task.answer_mode, result=message.text,
                                 is_pass=is_pass)
    if len(UserCallbackState.tasks) == 0:
        progress = await get_user_progress(session, user_id=message.from_user.id)
        await message.answer(f" {progress[0]} эпизод пройден ✅")
        user_class, user_become = await get_user_class(session, user_id=message.from_user.id)
        points = await get_user_points(session, user_id=message.from_user.id)
        if points:
            await message.answer(f"Поздравляю! На твоем счету - {points[0]} "
                                 f"е-коинов 💰\n"
                                 f"Узнай для чего они нужны "
                                 f"/coins_avail")
        if user_class == "Ребёнок":
            await message.answer('Перейдем к следующему эпизоду? 🤩', reply_markup=get_inline_next_block())
            return
        if user_class != "Ребёнок" and not user_become:
            await update_user_progress(session, user_id=message.from_user.id)
            await message.answer('Вам понравилось?', reply_markup=get_inline_is_like())
            return
        if user_class != "Ребёнок":
            await update_user_progress(session, user_id=message.from_user.id)
        progress = await get_progress_by_user_id(session, user_id=message.from_user.id)
        res = await get_block_id_by_progress(session, progress_block=progress[0])
        if not res:
            if user_become and user_class == "Родитель":
                await message.answer(congratulations, reply_markup=ReplyKeyboardRemove())
                await message.answer(pay_to_link, reply_markup=get_inline_parent_all_block_pay())
                return
            if user_class == "Педагог":
                await message.answer(congratulations, reply_markup=ReplyKeyboardRemove())
                await message.answer(you_should_be_partner,
                                     reply_markup=get_inline_teacher_all_block_referal())
                return
            await message.answer("Ссылка для ребенка")
            await message.answer(congratulations)
        return
    UserCallbackState.now_task = UserCallbackState.tasks[0]
    UserCallbackState.tasks = UserCallbackState.tasks[1:]
    if UserCallbackState.now_task.answer_mode == 'Описание изображения':
        await prepare_image_task(message, state, session)
    else:
        await prepare_test_tasks(message, state, session)


async def prepare_test_tasks(message, state, session):
    media_group = []
    caption_text = UserCallbackState.now_task.description + "\n\n" + UserCallbackState.now_task.answers + \
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
