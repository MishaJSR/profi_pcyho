from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import find_task, delete_task
from database.orm_query_block import get_block_by_id, get_block_id_by_callback
from database.orm_query_media_task import get_media_task_by_task_id
from database.orm_query_task import get_task_by_block_id
from keyboards.user.reply_user import start_kb
from keyboards.admin.reply_admin import start_kb, reset_kb
from handlers.admin.states import AdminManageTaskState, AdminStateDelete

user_callback_router = Router()

class UserCallbackState(StatesGroup):
    start_callback = State()
    image_callback = State()
    test_callback = State()
    tasks = []


@user_callback_router.callback_query()
async def check_button(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    callback_data = call.data
    block_id = await get_block_id_by_callback(session, callback_button_id=callback_data)
    tasks = await get_task_by_block_id(session, block_id=block_id[0])
    for task in tasks:
        UserCallbackState.tasks.append(task._data[0])
    now_task = UserCallbackState.tasks[0]
    if now_task.answer_mode == 'Описание изображения':
        photos = await get_media_task_by_task_id(session, task_id=now_task.id)
        print(photos)
    else:
        await state.set_state(UserCallbackState.test_callback)
        await call.message.answer(f"Подготовлено {len(tasks)} заданий")
    await call.answer('Вы выбрали задание')
    #9fa7e998-1700-46c9-8c8f-a82bd2fa4568


