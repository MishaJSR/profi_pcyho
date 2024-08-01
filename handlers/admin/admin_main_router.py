from aiogram.filters import Command
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from dotenv import find_dotenv, load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Users
from database.models_repository import UsersRepository
from database.orm_user.orm_query_user import delete_me_user
from database.orm_user.orm_query_user_task_progress import delete_all_user_progress
from filters.admin_filter import AdminFilter
from handlers.admin.admin_excel_loader_router import admin_excel_loader_router
from handlers.admin.admin_manage_sender_router import admin_manage_sender_router
from handlers.admin.admin_show_block import admin_show_block_router
from keyboards.admin.reply_admin import start_kb
from handlers.admin.states import AdminManageTaskState
from handlers.admin.admin_block_router import admin_block_router
from handlers.admin.manage_task_router import admin_add_task_router

admin_private_router = Router()
admin_private_router.include_routers(admin_block_router, admin_add_task_router, admin_manage_sender_router,
                                     admin_show_block_router, admin_excel_loader_router)
admin_private_router.message.filter(AdminFilter())
load_dotenv(find_dotenv())


@admin_private_router.message(Command('admin'))
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(text="Привет админ\n", reply_markup=start_kb())
    await state.set_state(AdminManageTaskState.start)


@admin_private_router.message(F.text == "Удалить меня")
async def fill_admin_state(message: types.Message, session: AsyncSession,  state: FSMContext):
    await delete_me_user(session, user_id=message.from_user.id)
    await delete_all_user_progress(session, user_id=message.from_user.id)
    await message.answer(text="Удалено", reply_markup=start_kb())


@admin_private_router.message(F.text == "Тест реп")
async def fill_admin_state(message: types.Message, session: AsyncSession,  state: FSMContext):
    field_filter1 = {
        "username": "Михаил",
        "is_subscribe": True
    }
    field_filter2 = {
        "username": "Михаил",
        "is_subscribe": True
    }
    user_fields = ["username", 'is_subscribe']
    res1 = await UsersRepository().get_one_by_filed(data="user_id", field_filter=field_filter1)
    res2 = await UsersRepository().get_all_by_filed(data="user_id", field_filter=field_filter2)
    res3 = await UsersRepository().get_one_by_fileds(data=user_fields, field_filter=field_filter1)
    print(res1)
    print(res2)
    print(res3)


