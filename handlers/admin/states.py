from aiogram.fsm.state import StatesGroup, State
from keyboards.admin.reply_admin import start_kb, back_kb, exam_kb, chapter_kb, answers_kb, answers_kb_end, about_kb, \
    answer_kb, restart_answer_kb, reset_kb, block_actions, send_media_kb, send_media_check_kb


class Admin_state(StatesGroup):
    start = State()
    exam = State()
    chapter = State()
    under_chapter = State()
    description = State()
    answers_checker = State()
    answers = State()
    answers_swap = State()
    answer = State()
    about = State()
    check_info = State()
    save_in_db = State()
    texts = {
        'Admin_state:start': ['Начало работы', start_kb],
        'Admin_state:exam': ['Выбор части', exam_kb],
        'Admin_state:chapter': ['Выбор модуля', chapter_kb],
        'Admin_state:under_chapter': ['Введите подмодуль', back_kb],
        'Admin_state:description': ['Введите условие задания', back_kb],
        'Admin_state:answers': ['Введите ответы', restart_answer_kb],
        'Admin_state:answers_swap': ['Введите вариант ответа', answers_kb_end],
        'Admin_state:answer': ['Введите ответ на задание', answer_kb],
        'Admin_state:about': ['Введите пояснение', about_kb],
        'Admin_state:check_info': ['Проверка', answers_kb_end],
        'Admin_state:save_in_db': ['Начало работы', start_kb],
    }
    default_data = {
        'exam': None,
        'chapter': None,
        'under_chapter': None,
        'description': None,
        'answers': '',
        'answer_mode': 'Квиз',
        'updated': '2024-03-19 11:44:19',
        'answer': None,
        'about': " ",
        'addition': ' ',
    }
    data = {}


class AdminStateSender(StatesGroup):
    start = State()
    choose_block_actions = State()
    text_state = State()
    media_state = State()
    prepare_to_load = State()
    confirm_state = State()
    name_block = State()
    texts = {
        'AdminStateSender:start': ['Начало работы', start_kb],
        'AdminStateSender:choose_block_actions': ['Выбор действий', block_actions],
        'AdminStateSender:text_state': ['Напишите текст рассылки', reset_kb],
        'AdminStateSender:media_state': ['Отправьте медиафайл', send_media_kb],
        'AdminStateSender:prepare_to_load': ['Если вы ошиблись с медиафайлом нажмите Назад', send_media_check_kb],
        'AdminStateSender:confirm_state': ['Выберите действие', send_media_kb],
        'AdminStateSender:name_block': ['Укажите краткое название блока', reset_kb],
    }
    text = ''
    photo = None
    photo_arr = []
    video_arr = []
    media = []
    video_id_list = []
    photo_counter = 0
    callback_for_task = None


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

