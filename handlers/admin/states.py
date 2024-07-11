from aiogram.fsm.state import StatesGroup, State
from keyboards.admin.reply_admin import start_kb, back_kb, chapter_kb, answers_kb, answers_kb_end, about_kb, \
    answer_kb, restart_answer_kb, reset_kb, block_actions, send_media_kb, send_media_check_kb


class Admin_state(StatesGroup):
    start = State()
    block_choose = State()
    type_task_choose = State()
    description = State()
    image_task_photo = State()
    answers_checker_keys = State()
    answers = State()
    answers_swap = State()
    answer = State()
    about = State()
    check_info = State()
    save_in_db = State()
    texts = {
        'Admin_state:start': ['Начало работы', start_kb],
        'Admin_state:block_choose': ['Выбор блока для задания', chapter_kb],
        'Admin_state:type_task_choose': ['Описание задания', type_task_choose],
        'Admin_state:description': ['Заполните форму', back_kb],
        'Admin_state:image_task_photo': ['Введите условие задания', back_kb],
        'Admin_state:answers_checker_keys': ['Введите ответы', restart_answer_kb],
        'Admin_state:answers_swap': ['Введите вариант ответа', answers_kb_end],
        'Admin_state:answer': ['Введите ответ на задание', answer_kb],
        'Admin_state:about': ['Введите пояснение', about_kb],
        'Admin_state:check_info': ['Проверка', answers_kb_end],
        'Admin_state:save_in_db': ['Начало работы', start_kb],
    }
    id_task = None
    photo_list = []
    photo_counter = 0
    caption = None


class AdminStateSender(StatesGroup):
    start = State()
    choose_block_actions = State()
    text_state = State()
    media_state = State()
    prepare_to_load = State()
    confirm_state = State()
    date_posting = State()
    name_block = State()

    texts = {
        'AdminStateSender:start': ['Начало работы', start_kb],
        'AdminStateSender:choose_block_actions': ['Выбор действий', block_actions],
        'AdminStateSender:text_state': ['Напишите текст рассылки', reset_kb],
        'AdminStateSender:media_state': ['Отправьте медиафайл', send_media_kb],
        'AdminStateSender:prepare_to_load': ['Если вы ошиблись с медиафайлом нажмите Назад', send_media_check_kb],
        'AdminStateSender:confirm_state': ['Выберите действие', send_media_kb],
        'AdminStateSender:name_block': ['Укажите краткое название блока', reset_kb],
        'AdminStateSender:date_posting': ['Укажите дату постинга', reset_kb],
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


class AdminStateDelete(StatesGroup):
    find_key = State()
    choose_task= State()
    confirm_delete = State()
    texts = {
        'AdminStateDelete:find_key': 'Ввод описания',
        'AdminStateDelete:choose_task': 'Выбор задания для удаления',
        'AdminStateDelete:confirm_delete': 'Подтверждение',
    }
    data = []

