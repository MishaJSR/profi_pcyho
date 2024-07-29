from aiogram.utils.keyboard import ReplyKeyboardBuilder

command_admin_list = ['Управление блоками', "Управление заданиями", 'Рассылка']
type_task_actions = ['Добавить задание', 'Удалить задание']
type_task = ['Описание изображения', 'Тест']
spam_actions = ['Отобразить статус блоков', 'Предпросмотр', "Отправить спам",
                "Выгрузка данных"]
excel_actions = ["Общая выгрузка", "Выгрузка данных родителей", "Выгрузка данных педагогов"]


def start_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    for el in command_admin_list:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def test_actions(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for el in type_task_actions:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def list_task_to_delete(data):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for el in data:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def block_pool_kb(data):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for el in data:
        test_kb.button(text=el)
    test_kb.adjust(1, 2)
    return test_kb.as_markup(resize_keyboard=True)


def type_task_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for el in type_task:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def send_media_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Оставить пустым')
    test_kb.button(text='Подготовить сообщение к рассылке')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def send_media_kb_veb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Оставить пустым')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def send_media_kb_task(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Оставить пустым')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def send_media_check_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Подготовить сообщение к рассылке')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def send_media_vebinar(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Подготовить спам к рассылке')
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
    test_kb.button(text='Добавить еще один пост')
    test_kb.button(text='Подтвердить и закончить добавление постов')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def spam_actions_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for el in spam_actions:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def excel_actions_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    for el in excel_actions:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)



def show_block_or_test(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Назад')
    test_kb.button(text='Содержание блока')
    test_kb.button(text='Содержание теста')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

