from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_task, orm_transport_base
from database.orm_query_block import get_block_for_add_task
from database.orm_query_media_task import add_media_task
from database.orm_query_task import add_task_image, add_task_test
from keyboards.admin.reply_admin import start_kb, answers_kb_end, about_kb, answers_kb, \
    answer_kb, back_kb, chapter_kb, type_task_kb, block_pool_kb, send_spam
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
        Admin_state.block_dict_id[block._data[0].block_name] = block._data[0].id
    await message.answer('Выберите блок для добавления задания', reply_markup=block_pool_kb(block_list))
    await state.set_state(Admin_state.block_choose)


@admin_add_task_router.message(Admin_state.block_choose, F.text)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.block_id = Admin_state.block_dict_id.get(message.text)
    Admin_state.task_type = None
    print(Admin_state.block_id)
    if not Admin_state.block_id:
        await message.answer(f'Такой блок не найден', reply_markup=start_kb())
    await message.answer(f'Выберите тип задания для блока {message.text}', reply_markup=type_task_kb())
    await state.set_state(Admin_state.type_task_choose)


@admin_add_task_router.message(Admin_state.type_task_choose, F.text == "Описание изображения")
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.task_type = message.text
    Admin_state.caption = None
    await message.answer(f'Добавьте описание к заданию', reply_markup=back_kb())
    await state.set_state(Admin_state.description)


@admin_add_task_router.message(Admin_state.description)
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.caption = message.text
    Admin_state.photo_list = []
    Admin_state.photo_counter = 0
    Admin_state.answers_to_load = None
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
    Admin_state.answers_to_load = message.text.lower()
    answers_keys = Admin_state.answers_to_load.split(' ')
    await message.answer(f'Найдены ключи\n')
    for el in answers_keys:
        await message.answer(f'{el}\n')
    await message.answer(f'Загрузить задание?', reply_markup=send_spam())
    await state.set_state(Admin_state.load_task)


@admin_add_task_router.message(Admin_state.load_task, F.text == 'Подтвердить')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        await add_task_image(session, block_id=Admin_state.block_id, description=Admin_state.caption,
                             answer_mode=Admin_state.task_type, answer=Admin_state.answers_to_load)
        for photo in Admin_state.photo_list:
            await add_photo_pool_task(session, Admin_state.block_id, photo.media)
        await message.answer('Задание загружено', reply_markup=start_kb())
    except Exception as e:
        print(e)
        await message.answer('Ошибка загрузки', reply_markup=start_kb())


async def add_photo_pool_task(session, task_id, file_id):
    await add_media_task(session, task_id=task_id, photo_id=file_id)


'''Test'''


@admin_add_task_router.message(Admin_state.type_task_choose, F.text == "Тест")
async def fill_admin_state(message: types.Message, state: FSMContext):
    Admin_state.task_type = message.text
    Admin_state.answers_test_to_load = None
    Admin_state.answer_test_to_load = None
    Admin_state.description_test_to_load = None
    await message.answer(f'Напишите тест в формате\nОписание:\nОписание задания\n'
                         f'Варианты ответа:\nВариант1\nВариант2\nВариант3\n'
                         f'Ответ:\nОтвет', reply_markup=back_kb())
    await state.set_state(Admin_state.description_test)


@admin_add_task_router.message(Admin_state.description_test, F.text)
async def fill_admin_state(message: types.Message, state: FSMContext):
    try:
        Admin_state.answers_test_to_load = '`'.join(message.text[message.text.find("Варианты ответа:") + 17:
                                                                 message.text.find("Ответ:")].split("\n")[:-1])
        Admin_state.description_test_to_load = message.text.split('\n')[1]
        Admin_state.answer_test_to_load = message.text.replace('\n', "").split('Ответ:')[1]
        await message.answer(f'Описание:\n{Admin_state.description_test_to_load}\n'
                             f'Варианты ответа:\n{Admin_state.answers_test_to_load}\n'
                             f'Ответ:\n{Admin_state.answer_test_to_load}')
        await message.answer(f'Все верно?', reply_markup=send_spam())
        await state.set_state(Admin_state.confirm_test)
    except Exception as e:
        await message.answer(f'Ошибка прочтения', reply_markup=start_kb())
        await state.set_state(Admin_state.start)


@admin_add_task_router.message(Admin_state.confirm_test, F.text == "Подтвердить")
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        await add_task_test(session, block_id=Admin_state.block_id, description=Admin_state.description_test_to_load,
                            answer_mode=Admin_state.task_type, answers=Admin_state.answers_test_to_load,
                            answer=Admin_state.answer_test_to_load)
        await message.answer('Успешная загрузка', reply_markup=start_kb())
    except Exception as e:
        print(e)
        await message.answer('Ошибка загрузки', reply_markup=start_kb())


'''Test'''
