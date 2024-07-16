from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import emoji

start_but = ['Когда будет следующий блок?']


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

def get_inline_veb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Пройти задание по курсу', callback_data='asdsaafafadasdasdafaac',
                   url='https://t.me/humanitiessociety')
    return builder.as_markup()


