from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InputMediaPhoto, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_block import get_block_id_by_callback
from database.orm_query_media_task import get_media_task_by_task_id
from database.orm_query_task import get_task_by_block_id
from database.orm_query_user import update_user_progress, update_user_points
from database.orm_query_user_task_progress import set_user_task_progress, get_task_progress_by_user_id
from keyboards.user.reply_user import start_kb, answer_kb

user_callback_router = Router()


class UserCallbackState(StatesGroup):
    start_callback = State()
    image_callback = State()
    test_callback = State()
    tasks = []
    count_tasks = None
    block_id = None
    now_task = None
    list_of_answers = []


@user_callback_router.callback_query()
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    UserCallbackState.tasks = []
    UserCallbackState.block_id = None
    UserCallbackState.now_task = None
    callback_data = call.data
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
        await prepare_test_tasks(call.message, state)
        await call.answer('Вы выбрали задание')


@user_callback_router.message(UserCallbackState.image_callback, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    is_pass = is_part_in_list(message.text, UserCallbackState.now_task.answer.split(" "))
    if is_pass:
        await message.answer(f"Поздравляем !!!\nВы получили {UserCallbackState.now_task.points_for_task} очков")
        await update_user_points(session, user_id=message.from_user.id,
                                 points=UserCallbackState.now_task.points_for_task)
    await update_user_task_progress_and_go_to_next(message, session, state, is_pass)


@user_callback_router.message(UserCallbackState.test_callback, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Ошибка ввода, повторите снова")
        return
    is_pass = False
    if int(UserCallbackState.now_task.answer) == int(message.text):
        is_pass = True
        await message.answer(f"Поздравляю Вы заработали {UserCallbackState.now_task.points_for_task} очков")
        await update_user_points(session, user_id=message.from_user.id,
                                 points=UserCallbackState.now_task.points_for_task)
    await update_user_task_progress_and_go_to_next(message, session, state, is_pass)


async def update_user_task_progress_and_go_to_next(message, session, state, is_pass):
    await set_user_task_progress(session, user_id=message.from_user.id, task_id=UserCallbackState.now_task.id,
                                 username=message.from_user.full_name, block_id=UserCallbackState.now_task.block_id,
                                 answer_mode=UserCallbackState.now_task.answer_mode, result=message.text,
                                 is_p1ass=is_pass)
    if len(UserCallbackState.tasks) == 0:
        await message.answer("Все задания пройдены", reply_markup=start_kb())
        await update_user_progress(session, user_id=message.from_user.id)
        return
    UserCallbackState.now_task = UserCallbackState.tasks[0]
    UserCallbackState.tasks = UserCallbackState.tasks[1:]
    if UserCallbackState.now_task.answer_mode == 'Описание изображения':
        await prepare_image_task(message, state, session)
    else:
        await prepare_test_tasks(message, state)

async def prepare_test_tasks(message, state):
    res_message = f"{UserCallbackState.now_task.description}\n"
    UserCallbackState.list_of_answers = []
    UserCallbackState.list_of_answers = UserCallbackState.now_task.answers.split('`')
    for index, answer in enumerate(UserCallbackState.list_of_answers):
        res_message += f"{index + 1}. {answer}\n"
    await message.answer(res_message, reply_markup=answer_kb(data=len(UserCallbackState.list_of_answers)))
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
