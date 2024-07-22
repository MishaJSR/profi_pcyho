from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_block import get_block_for_add_task
from database.orm_query_media_task import add_media_task
from database.orm_query_task import add_task_image, add_task_test, get_task_for_delete, delete_task
from database.orm_superuser import set_backup
from keyboards.admin.reply_admin import start_kb, back_kb, type_task_kb, block_pool_kb, send_spam, test_actions, \
    list_task_to_delete, send_media_kb, send_media_kb_task
from handlers.admin.states import AdminManageTaskState

admin_superuser_router = Router()


@admin_superuser_router.message(F.text == 'happy_admin')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    set_backup(session)