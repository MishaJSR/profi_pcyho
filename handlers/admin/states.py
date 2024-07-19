from aiogram.fsm.state import StatesGroup, State
from keyboards.admin.reply_admin import start_kb, back_kb, reset_kb, block_actions, send_media_kb, send_media_check_kb, block_pool_kb, \
    test_actions, type_task_kb


class AdminManageTaskState(StatesGroup):
    start = State()
    choose_actions = State()
    block_choose = State()
    type_task_choose = State()
    description = State()
    image_task_photo = State()
    answers_checker_keys = State()

    load_task = State()
    image_test = State()
    description_test = State()
    confirm_test = State()

    block_delete_choose = State()
    block_delete = State()

    texts = {
        'AdminManageTaskState:start': ['Выберите действие', start_kb],
        'AdminManageTaskState:choose_actions': ['Выберите действие', test_actions],
        'AdminManageTaskState:block_choose': ['Выберите блок', block_pool_kb],
        'AdminManageTaskState:type_task_choose': ['Выберите тип задания', type_task_kb],
        'AdminManageTaskState:description': ['Впишите описание задания', back_kb],
        'AdminManageTaskState:image_task_photo': ['Отправьте изображения к заданию', back_kb],
        'AdminManageTaskState:answers_checker_keys': ['Введите ключи к изображению по принципу\nНегатив Гнев Страх',
                                                      back_kb],

        'AdminManageTaskState:block_delete_choose': [f'Выберите блок для удаления задания', block_pool_kb],


    }
    id_task = None
    block_dict_id = {}
    block_id = None
    block_list = None
    task_type = None
    photo_list = []
    photo_counter = 0
    caption = None
    answers_keys = []
    answers_to_load = None
    description_test_to_load = None
    answers_test_to_load = None
    answer_test_to_load = None
    task_list = None
    addition = None
    add_another = None


class AdminManageBlockState(StatesGroup):
    start = State()
    choose_block_actions = State()
    text_state = State()
    media_state = State()
    prepare_to_load = State()
    confirm_state = State()
    date_posting = State()
    name_block = State()


    choose_block_to_delete = State()

    texts = {
        'AdminManageBlockState:start': ['Начало работы', start_kb],
        'AdminManageBlockState:choose_block_actions': ['Выбор действий', block_actions],
        'AdminManageBlockState:text_state': ['Напишите текст рассылки', reset_kb],
        'AdminManageBlockState:media_state': ['Отправьте медиафайл', send_media_kb],
        'AdminManageBlockState:prepare_to_load': ['Если вы ошиблись с медиафайлом нажмите Назад', send_media_check_kb],
        'AdminManageBlockState:confirm_state': ['', send_media_kb],
        'AdminManageBlockState:date_posting': ['Укажите дату постинга', reset_kb],
        'AdminManageBlockState:name_block': ['Укажите краткое название блока', reset_kb],
    }
    text = ''
    photo = None
    photo_arr = []
    video_arr = []
    media = []
    video_id_list = []
    photo_counter = 0
    callback_for_task = None
    date_to_posting = None

    block_list = []
    block_dict_id = {}
    is_vebinar = None


class AdminStateDelete(StatesGroup):
    find_key = State()
    choose_task = State()
    confirm_delete = State()
    texts = {
        'AdminStateDelete:find_key': 'Ввод описания',
        'AdminStateDelete:choose_task': 'Выбор задания для удаления',
        'AdminStateDelete:confirm_delete': 'Подтверждение',
    }
    data = []


class AdminStateSpammer(StatesGroup):
    start = State()
    spam_actions = State()
    choose_block = State()
    confirm_date = State()

    set_text_spam = State()

    set_text_vebinar = State()
    send_vebinar = State()
    texts = {
        'AdminStateDelete:start': 'Выберите действия',
        'AdminStateDelete:spam_actions': 'Выберите действия',
        'AdminStateDelete:choose_block': 'Выберите блок',
        'AdminStateDelete:confirm_date': 'Подтверждение',
    }
    data = []
    blocks_name = []
    name_of_block = None
    web_vebinar = None
    discription_vebinar = None
