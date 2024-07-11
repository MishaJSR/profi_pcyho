from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_task, orm_transport_base
from database.orm_query_block import get_block_for_add_task
from keyboards.admin.reply_admin import start_kb, answers_kb_end, about_kb, answers_kb, \
    answer_kb, back_kb, chapter_kb, type_task_kb, block_pool_kb
from handlers.admin.states import Admin_state

admin_add_task_router = Router()


@admin_add_task_router.message(F.text == 'Управление заданиями')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_block_for_add_task(session)
    except Exception as e:
        await message.answer('Ошибка подключения к базе данных блоков. Возможно у вас отсутствуют блоки')
        return
    block_list = []
    for block in res:
        block_list.append(block._data[0].block_name)
    await message.answer('Выберите блок для добавления задания', reply_markup=block_pool_kb(block_list))
    await state.set_state(Admin_state.block_choose)


@admin_add_task_router.message(Admin_state.block_choose, F.text)
async def fill_admin_state(message: types.Message, state: FSMContext):
    await message.answer(f'Выберите тип задания для блока {message.text}', reply_markup=type_task_kb())
    await state.set_state(Admin_state.type_task_choose)


@admin_add_task_router.message(Admin_state.type_task_choose, F.text == "Описание изображения")
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.caption = None
    await message.answer(f'Добавьте описание к заданию', reply_markup=back_kb())
    await state.set_state(Admin_state.description)


@admin_add_task_router.message(Admin_state.description)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.caption = message.text
    Admin_state.photo_list = []
    Admin_state.photo_counter = 0
    await message.answer(f'Отправьте изображения к заданию', reply_markup=back_kb())
    await state.set_state(Admin_state.image_task_photo)



@admin_add_task_router.message(Admin_state.image_task_photo)
async def fill_admin_state(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Ошибка ввода, необходимо отправить изображения")
        return
    try:
        Admin_state.photo_list.append(InputMediaPhoto(type='photo', media=message.photo[-1].file_id))
    except Exception as e:
        await message.answer("Ошибка при получении медиафайла", reply_markup=start_kb())
        return
    if Admin_state.photo_counter == 0:
        Admin_state.photo_counter += 1
        await message.answer("Изображения получены")
        await message.answer(f'Введите ключи к изображению по принципу\nНегатив Гнев Страх', reply_markup=back_kb())
        await state.set_state(Admin_state.answers_checker_keys)


@admin_add_task_router.message(Admin_state.answers_checker_keys, F.text)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.caption = message.text
    Admin_state.photo_list = []
    Admin_state.photo_counter = 0
    await message.answer(f'Отправьте изображения к заданию', reply_markup=back_kb())
    await state.set_state(Admin_state.image_task_photo)












@admin_add_task_router.message(Admin_state.type_task_choose, F.text == "Тест")
async def fill_admin_state(message: types.Message, state: FSMContext):

    await message.answer(f'Выберите тип задания для блока {message.text}', reply_markup=type_task_kb())
    await state.set_state(Admin_state.type_task_choose)