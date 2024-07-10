from aiogram.utils.keyboard import ReplyKeyboardBuilder
from keyboards.user.reply_user import main_but, modules

command_admin_list = ['Управление блоками', "Управление заданиями", 'Рассылка']


def start_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    for el in command_admin_list:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def exam_kb(data=main_but):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for el in data:
        test_kb.button(text=el)
    test_kb.adjust(1, 2)
    return test_kb.as_markup(resize_keyboard=True)


def chapter_kb(data=modules):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for el in data:
        test_kb.button(text=el)
    test_kb.adjust(1, 2)
    return test_kb.as_markup(resize_keyboard=True)


def answers_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Закончить ввод')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def answers_kb_end():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Подтвердить')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def answer_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    return test_kb.as_markup(resize_keyboard=True)


def restart_answer_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Начать снова')
    return test_kb.as_markup(resize_keyboard=True)


def about_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Оставить пустым')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def send_img_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Отмена')
    test_kb.button(text='Оставить пустым')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def send_img_repeat_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Отмена')
    test_kb.button(text='Добавить ещё одно изображение')
    test_kb.button(text='Подготовить сообщение к рассылке')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def send_media_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Оставить пустым')
    test_kb.button(text='Подготовить сообщение к рассылке')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def send_media_check_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Подготовить сообщение к рассылке')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def send_video_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Оставить пустым')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def send_video_repeat_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Добавить ещё одно видео')
    test_kb.button(text='Подготовить сообщение к рассылке')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def back_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def block_actions(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Добавить блок')
    test_kb.button(text='Удалить блок')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def reset_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def send_spam(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Подтвердить')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def prepare_to_spam(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Подтвердить')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)
