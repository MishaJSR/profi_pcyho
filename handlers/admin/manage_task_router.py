from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_task, orm_transport_base
from database.orm_query_block import get_block_for_add_task
from database.orm_query_media_task import add_media_task
from database.orm_query_task import add_task_image, add_task_test, get_task_for_delete, delete_task
from keyboards.admin.reply_admin import start_kb, answers_kb_end, about_kb, answers_kb, \
    answer_kb, back_kb, chapter_kb, type_task_kb, block_pool_kb, send_spam, test_actions, list_task_to_delete
from handlers.admin.states import AdminManageTaskState

admin_add_task_router = Router()


@admin_add_task_router.message(F.text == 'Управление заданиями')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminManageTaskState.block_list = None
    await message.answer("Выберите действие", reply_markup=test_actions())
    await state.set_state(AdminManageTaskState.choose_actions)
    current_state = await state.get_state()
    print(current_state)


@admin_add_task_router.message(StateFilter(AdminManageTaskState), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    print(current_state)

    if current_state == AdminManageTaskState.type_task_choose:
        await message.answer(text='Выберите блок для добавления задания',
                             reply_markup=block_pool_kb(AdminManageTaskState.block_list))
        await state.set_state(AdminManageTaskState.block_choose)
        return

    if current_state == AdminManageTaskState.answers_checker_keys:
        AdminManageTaskState.photo_list = []
        AdminManageTaskState.photo_counter = 0
        AdminManageTaskState.answers_to_load = None

    if current_state == AdminManageTaskState.description_test:
        await message.answer(text='Выберите тип задания',
                             reply_markup=type_task_kb())
        await state.set_state(AdminManageTaskState.type_task_choose)
        return

    if current_state == AdminManageTaskState.block_delete_choose:
        await message.answer(text='Выберите действие',
                             reply_markup=test_actions())
        await state.set_state(AdminManageTaskState.choose_actions)
        return

    if current_state == AdminManageTaskState.block_delete:
        await message.answer(text='Выберите блок для удаления задания',
                             reply_markup=block_pool_kb(AdminManageTaskState.block_list))
        await state.set_state(AdminManageTaskState.block_delete_choose)
        return

    previous = None
    for step in AdminManageTaskState.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому шагу \n{AdminManageTaskState.texts[previous.state][0]}",
                                 reply_markup=AdminManageTaskState.texts[previous.state][1]())
            return
        previous = step


@admin_add_task_router.message(AdminManageTaskState.choose_actions, F.text == 'Добавить задание')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_block_for_add_task(session)
    except Exception as e:
        await message.answer('Ошибка подключения к базе данных блоков. Возможно у вас отсутствуют блоки')
        return
    AdminManageTaskState.block_list = []
    for block in res:
        AdminManageTaskState.block_list.append(block._data[0].block_name)
        AdminManageTaskState.block_dict_id[block._data[0].block_name] = block._data[0].id
    await message.answer('Выберите блок для добавления задания',
                         reply_markup=block_pool_kb(AdminManageTaskState.block_list))
    await state.set_state(AdminManageTaskState.block_choose)


@admin_add_task_router.message(AdminManageTaskState.block_choose, F.text)
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminManageTaskState.block_id = AdminManageTaskState.block_dict_id.get(message.text)
    AdminManageTaskState.task_type = None
    if not AdminManageTaskState.block_id:
        await message.answer(f'Такой блок не найден', reply_markup=start_kb())
        return
    await message.answer(f'Выберите тип задания для блока {message.text}', reply_markup=type_task_kb())
    await state.set_state(AdminManageTaskState.type_task_choose)


"""Image"""


@admin_add_task_router.message(AdminManageTaskState.type_task_choose, F.text == "Описание изображения")
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminManageTaskState.task_type = message.text
    AdminManageTaskState.caption = None
    await message.answer(f'Добавьте описание к заданию', reply_markup=back_kb())
    await state.set_state(AdminManageTaskState.description)


@admin_add_task_router.message(AdminManageTaskState.description)
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminManageTaskState.caption = message.text
    AdminManageTaskState.photo_list = []
    AdminManageTaskState.photo_counter = 0
    AdminManageTaskState.answers_to_load = None
    await message.answer(f'Отправьте изображения к заданию', reply_markup=back_kb())
    await state.set_state(AdminManageTaskState.image_task_photo)


@admin_add_task_router.message(AdminManageTaskState.image_task_photo)
async def fill_admin_state(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Ошибка ввода, необходимо отправить изображения")
        return
    try:
        AdminManageTaskState.photo_list.append(InputMediaPhoto(type='photo', media=message.photo[-1].file_id))
    except Exception as e:
        await message.answer("Ошибка при получении медиафайла", reply_markup=start_kb())
        return
    if AdminManageTaskState.photo_counter == 0:
        AdminManageTaskState.photo_counter += 1
        await message.answer("Изображения получены")
        await message.answer(f'Введите ключи к изображению по принципу\nНегатив Гнев Страх', reply_markup=back_kb())
        await state.set_state(AdminManageTaskState.answers_checker_keys)


@admin_add_task_router.message(AdminManageTaskState.answers_checker_keys, F.text)
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminManageTaskState.answers_to_load = message.text.lower()
    answers_keys = AdminManageTaskState.answers_to_load.split(' ')
    await message.answer(f'Найдены ключи\n')
    for el in answers_keys:
        await message.answer(f'{el}\n')
    await message.answer(f'Загрузить задание?', reply_markup=send_spam())
    await state.set_state(AdminManageTaskState.load_task)


@admin_add_task_router.message(AdminManageTaskState.load_task, F.text == 'Подтвердить')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        await add_task_image(session, block_id=AdminManageTaskState.block_id, description=AdminManageTaskState.caption,
                             answer_mode=AdminManageTaskState.task_type, answer=AdminManageTaskState.answers_to_load)
        for photo in AdminManageTaskState.photo_list:
            await add_photo_pool_task(session, AdminManageTaskState.block_id, photo.media)
        await message.answer('Задание загружено', reply_markup=start_kb())
        await state.set_state(AdminManageTaskState.start)
    except Exception as e:
        print(e)
        await message.answer('Ошибка загрузки', reply_markup=start_kb())


async def add_photo_pool_task(session, task_id, file_id):
    await add_media_task(session, task_id=task_id, photo_id=file_id)


"""Image"""

'''Test'''


@admin_add_task_router.message(AdminManageTaskState.type_task_choose, F.text == "Тест")
async def fill_admin_state(message: types.Message, state: FSMContext):
    AdminManageTaskState.task_type = message.text
    AdminManageTaskState.answers_test_to_load = None
    AdminManageTaskState.answer_test_to_load = None
    AdminManageTaskState.description_test_to_load = None
    await message.answer(f'Напишите тест в формате\nОписание:\nОписание задания\n'
                         f'Варианты ответа:\nВариант1\nВариант2\nВариант3\n'
                         f'Ответ:\nОтвет', reply_markup=back_kb())
    await state.set_state(AdminManageTaskState.description_test)


@admin_add_task_router.message(AdminManageTaskState.description_test, F.text)
async def fill_admin_state(message: types.Message, state: FSMContext):
    try:
        AdminManageTaskState.answers_test_to_load = '`'.join(message.text[message.text.find("Варианты ответа:") + 17:
                                                                          message.text.find("Ответ:")].split("\n")[:-1])
        AdminManageTaskState.description_test_to_load = message.text.split('\n')[1]
        AdminManageTaskState.answer_test_to_load = message.text.replace('\n', "").split('Ответ:')[1]
        await message.answer(f'Описание:\n{AdminManageTaskState.description_test_to_load}\n'
                             f'Варианты ответа:\n{AdminManageTaskState.answers_test_to_load}\n'
                             f'Ответ:\n{AdminManageTaskState.answer_test_to_load}')
        await message.answer(f'Все верно?', reply_markup=send_spam())
        await state.set_state(AdminManageTaskState.confirm_test)
    except Exception as e:
        await message.answer(f'Ошибка прочтения\n')
        await message.answer(f'Напишите тест в формате\nОписание:\nОписание задания\n'
                             f'Варианты ответа:\nВариант1\nВариант2\nВариант3\n'
                             f'Ответ:\nОтвет', reply_markup=back_kb())


@admin_add_task_router.message(AdminManageTaskState.confirm_test, F.text == "Подтвердить")
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        await add_task_test(session, block_id=AdminManageTaskState.block_id,
                            description=AdminManageTaskState.description_test_to_load,
                            answer_mode=AdminManageTaskState.task_type,
                            answers=AdminManageTaskState.answers_test_to_load,
                            answer=AdminManageTaskState.answer_test_to_load)
        await message.answer('Успешная загрузка', reply_markup=start_kb())
    except Exception as e:
        print(e)
        await message.answer('Ошибка загрузки', reply_markup=start_kb())
    finally:
        await state.set_state(AdminManageTaskState.start)



'''Test'''

'''Delete task'''


@admin_add_task_router.message(AdminManageTaskState.choose_actions, F.text == 'Удалить задание')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_block_for_add_task(session)
    except Exception as e:
        await message.answer('Ошибка подключения к базе данных блоков. Возможно у вас отсутствуют блоки')
        return
    AdminManageTaskState.block_list = []
    for block in res:
        AdminManageTaskState.block_list.append(block._data[0].block_name)
        AdminManageTaskState.block_dict_id[block._data[0].block_name] = block._data[0].id
    await message.answer('Выберите блок для удаления задания', reply_markup=block_pool_kb(AdminManageTaskState.block_list))
    await state.set_state(AdminManageTaskState.block_delete_choose)


@admin_add_task_router.message(AdminManageTaskState.block_delete_choose)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminManageTaskState.block_id = AdminManageTaskState.block_dict_id.get(message.text)
    if not AdminManageTaskState.block_id:
        await message.answer(f'Такой блок не найден', reply_markup=start_kb())
        return
    try:
        res = await get_task_for_delete(session, task_id=AdminManageTaskState.block_id)
        AdminManageTaskState.task_list = {}
        for task in res:
            AdminManageTaskState.task_list[task._data[0].description] = task._data[0].id
        await message.answer(f'Выберите задание для удаления',
                             reply_markup=list_task_to_delete(list(AdminManageTaskState.task_list.keys())))
        await state.set_state(AdminManageTaskState.block_delete)
    except Exception as e:
        await message.answer('Такой блок не найден', reply_markup=start_kb())


@admin_add_task_router.message(AdminManageTaskState.block_delete, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    id_task_to_delete = AdminManageTaskState.task_list.get(message.text)
    try:
        res = await delete_task(session, task_id=id_task_to_delete)
        await message.answer("Задание успешно удалено", reply_markup=start_kb())
    except Exception as e:
        print(e)
        await message.answer("Ошибка удаления", reply_markup=start_kb())
    finally:
        await state.set_state(AdminManageTaskState.start)


'''Delete task'''
