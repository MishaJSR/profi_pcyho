from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_task, orm_transport_base
from keyboards.user.reply_user import start_kb
from keyboards.admin.reply_admin import start_kb, answers_kb_end, about_kb, answers_kb, \
    answer_kb, back_kb, chapter_kb, exam_kb
from handlers.admin.states import Admin_state

admin_add_task_router = Router()


@admin_add_task_router.message(F.text == '"Управление заданиями"')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer('Выберите раздел подготовки', reply_markup=exam_kb())
    await state.set_state(Admin_state.exam)

