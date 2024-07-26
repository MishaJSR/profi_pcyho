from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_block import get_block_for_add_task
from database.orm_query_media_task import add_media_task
from database.orm_query_task import add_task_image, add_task_test, get_task_for_delete, delete_task
from keyboards.admin.reply_admin import start_kb, back_kb, type_task_kb, block_pool_kb, send_spam, test_actions, \
    list_task_to_delete, send_media_kb, send_media_kb_task
from handlers.admin.states import AdminManageTaskState

admin_add_task_router = Router()


@admin_add_task_router.message(F.text == 'Управление заданиями')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    AdminManageTaskState.block_list = None
    await message.answer("Выберите действие", reply_markup=test_actions())
    await state.set_state(AdminManageTaskState.choose_actions)
    current_state = await state.get_state()


@admin_add_task_router.message(StateFilter(AdminManageTaskState), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

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

    if current_state == AdminManageTaskState.confirm_test or current_state == AdminManageTaskState.image_test:
        AdminManageTaskState.task_type = message.text
        AdminManageTaskState.answers_test_to_load = None
        AdminManageTaskState.answer_test_to_load = None
        AdminManageTaskState.description_test_to_load = None
        AdminManageTaskState.addition = None
        AdminManageTaskState.add_another = None
        AdminManageTaskState.photo_list = []
        AdminManageTaskState.photo_counter = 0
        await message.answer(f'Напишите тест в формате\nОписание задания\n\n'
                             f'1. Вариант1\n2: Вариант2\n3: Вариант3\n\n'
                             f'13\n\nВыбери правильные ответы и напиши их цифры', reply_markup=back_kb())
        await state.set_state(AdminManageTaskState.description_test)
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
        task_id = await add_task_image(session, block_id=AdminManageTaskState.block_id, description=AdminManageTaskState.caption,
                             answer_mode=AdminManageTaskState.task_type, answer=AdminManageTaskState.answers_to_load)
        for photo in AdminManageTaskState.photo_list:
            await add_photo_pool_task(session, task_id, photo.media)
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
    AdminManageTaskState.add_another = None
    AdminManageTaskState.addition = None
    AdminManageTaskState.photo_list = []
    AdminManageTaskState.photo_counter = 0
    await message.answer(f'Напишите тест в формате\nОписание задания\n\n'
                         f'1. Вариант1\n2: Вариант2\n3: Вариант3\n\n'
                         f'13\n\nВыбери правильные ответы и напиши их цифры', reply_markup=back_kb())
    await state.set_state(AdminManageTaskState.description_test)


@admin_add_task_router.message(AdminManageTaskState.description_test, F.text)
async def fill_admin_state(message: types.Message, state: FSMContext):
    try:
        arr_abz = message.text.split('\n\n')
        index_answer = 0
        for index, el in enumerate(arr_abz):
            if el.isdigit():
                index_answer = index
        index_answers = index_answer - 1
        if index_answer == (len(arr_abz) - 1):
            index_addition = None
        else:
            index_addition = -1
        index_description = index_answers - 1
        if index_description == 0:
            AdminManageTaskState.add_another = ""
        else:
            AdminManageTaskState.add_another = message.text.split('\n\n')[:index_description]
        AdminManageTaskState.description_test_to_load = message.text.split('\n\n')[index_description]
        AdminManageTaskState.answers_test_to_load = message.text.split('\n\n')[index_answers]
        AdminManageTaskState.answer_test_to_load = message.text.split('\n\n')[index_answer]
        if not AdminManageTaskState.answer_test_to_load.isdigit():
            await message.answer("Не могу найти ответ")
            raise Exception
        if index_addition:
            AdminManageTaskState.addition = message.text.split('\n\n')[index_addition]
        else:
            AdminManageTaskState.addition = ""
        await message.answer("Отправьте изображение", reply_markup=send_media_kb_task())
        await state.set_state(AdminManageTaskState.image_test)
    except Exception as e:
        await message.answer(f'Ошибка прочтения\n')
        await message.answer(f'Напишите тест в формате\nОписание задания\n\n'
                             f'1. Вариант1\n2: Вариант2\n3: Вариант3\n\n'
                             f'13\n\nВыбери правильные ответы и напиши их цифры', reply_markup=back_kb())


@admin_add_task_router.message(AdminManageTaskState.image_test)
async def fill_admin_state(message: types.Message, state: FSMContext):
    if message.text == "Оставить пустым":
        if isinstance(AdminManageTaskState.add_another, str):
            another = AdminManageTaskState.add_another
        elif len(AdminManageTaskState.add_another) == 0:
            another = ""
        else:
            another = "".join(AdminManageTaskState.add_another)
            another += "\n\n"
        text = another + '*' + AdminManageTaskState.description_test_to_load + "*\n\n" + AdminManageTaskState.answers_test_to_load + \
               '\n\n' + AdminManageTaskState.addition
        await message.answer(text, parse_mode="Markdown")
        AdminManageTaskState.description_test_to_load = another + '*' + AdminManageTaskState.description_test_to_load + "*"
        await message.answer(f'Все верно?', reply_markup=send_spam())
        await state.set_state(AdminManageTaskState.confirm_test)
        return
    if not message.photo:
        await message.answer("Ошибка ввода, необходимо отправить изображение")
        return
    try:
        if isinstance(AdminManageTaskState.add_another, str):
            another = AdminManageTaskState.add_another
        elif len(AdminManageTaskState.add_another) == 0:
            another = ""
        else:
            another = "\n\n".join(AdminManageTaskState.add_another)
            another += "\n\n"
        AdminManageTaskState.description_test_to_load = another + '*' + AdminManageTaskState.description_test_to_load + "*"
        text = AdminManageTaskState.description_test_to_load + "\n\n" + AdminManageTaskState.answers_test_to_load + \
               '\n\n' + AdminManageTaskState.addition
        if AdminManageTaskState.photo_counter == 0:
            AdminManageTaskState.photo_list.append(InputMediaPhoto(type='photo', media=message.photo[-1].file_id,
                                                                   caption=text, parse_mode="Markdown"))
        else:
            AdminManageTaskState.photo_list.append(InputMediaPhoto(type='photo', media=message.photo[-1].file_id))
    except Exception as e:
        await message.answer("Ошибка при получении медиафайла", reply_markup=start_kb())
        return
    if AdminManageTaskState.photo_counter == 0:
        AdminManageTaskState.photo_counter += 1
        await message.answer("Изображения получены")
        await message.answer_media_group(media=AdminManageTaskState.photo_list)
        await message.bot.send_media_group(chat_id=-1002164443199, media=AdminManageTaskState.photo_list)
        await message.answer(f'Все верно?', reply_markup=send_spam())
        await state.set_state(AdminManageTaskState.confirm_test)





@admin_add_task_router.message(AdminManageTaskState.confirm_test, F.text == "Подтвердить")
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        task_id = await add_task_test(session, block_id=AdminManageTaskState.block_id,
                            description=AdminManageTaskState.description_test_to_load,
                            answer_mode=AdminManageTaskState.task_type,
                            answers=AdminManageTaskState.answers_test_to_load,
                            answer=AdminManageTaskState.answer_test_to_load,
                            addition=AdminManageTaskState.addition)
        for photo in AdminManageTaskState.photo_list:
            await add_photo_pool_task(session, task_id, photo.media)
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
            AdminManageTaskState.task_list[task._data[0].id] = task._data[0].description[:19]
        await message.answer(f'Выберите задание для удаления',
                             reply_markup=list_task_to_delete(list(AdminManageTaskState.task_list.values())))
        await state.set_state(AdminManageTaskState.block_delete)
    except Exception as e:
        await message.answer('Такой блок не найден', reply_markup=start_kb())


@admin_add_task_router.message(AdminManageTaskState.block_delete, F.text)
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    id_task_to_delete = get_key_by_value(AdminManageTaskState.task_list, message.text[:20])
    if not id_task_to_delete:
        await message.answer("Ошибка ввода", reply_markup=start_kb())
        await state.set_state(AdminManageTaskState.start)
        return
    try:
        res = await delete_task(session, task_id=id_task_to_delete)
        await message.answer("Задание успешно удалено", reply_markup=start_kb())
    except Exception as e:
        print(e)
        await message.answer("Ошибка удаления", reply_markup=start_kb())
    finally:
        await state.set_state(AdminManageTaskState.start)

def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None
'''Delete task'''
