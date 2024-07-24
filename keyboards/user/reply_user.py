from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import emoji

start_but = ['Когда будет следующий блок?']
users_pool = ['Ребёнок', 'Родитель', 'Преподаватель']

def start_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    for el in start_but:
        test_kb.button(text=el)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def empty_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def answer_kb(data=None):
    test_kb = ReplyKeyboardBuilder()
    for el in range(data):
        text = str(el + 1)
        test_kb.button(text=text)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)



def send_contact_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Поделиться номером', request_contact=True)
    test_kb.button(text='Пропустить')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def send_name_user_kb():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Пропустить')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)

def users_pool_kb():
    test_kb = ReplyKeyboardBuilder()
    for text in users_pool:
        test_kb.button(text=text)
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)


def parent_permission():
    test_kb = ReplyKeyboardBuilder()
    test_kb.button(text='Да, я даю согласие')
    test_kb.button(text='Нет, я против')
    test_kb.adjust(1, 1)
    return test_kb.as_markup(resize_keyboard=True)