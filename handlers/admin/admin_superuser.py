from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_superuser import set_backup

admin_superuser_router = Router()


@admin_superuser_router.message(F.text == 'happy_admin')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    pass