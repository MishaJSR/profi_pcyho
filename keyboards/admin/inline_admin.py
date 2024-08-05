import os

import emoji
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import find_dotenv, load_dotenv
from utils.common.message_constant import referal_link, course_link, happy_link

load_dotenv(find_dotenv())
course_link = course_link
course_referal = referal_link


def get_inline(is_second=False, callback_data=None):
    builder = InlineKeyboardBuilder()
    if is_second:
        builder.button(text='Перейти к заданиям 💪', callback_data=callback_data)
    else:
        builder.button(text='Да 💪', callback_data=callback_data)
    builder.adjust(1, 1)
    return builder.as_markup()


def get_inline_to_tasks():
    builder = InlineKeyboardBuilder()
    builder.button(text='Перейти к заданиям 💪', callback_data="start_task")
    builder.adjust(1, 1)
    return builder.as_markup()

def get_inline_vebinar(url):
    builder = InlineKeyboardBuilder()
    builder.button(text='Перейти на вебинар', callback_data='asdsaafafadasdasdafaac',
                   url=url)
    return builder.as_markup()


def get_inline_parent():
    builder = InlineKeyboardBuilder()
    builder.button(text='Перейти к регистрации', callback_data='parent_registration')
    return builder.as_markup()


def get_inline_parent_all_block():
    builder = InlineKeyboardBuilder()
    builder.button(text='Оплатить', callback_data='effeefwwefefe',
                   url=course_link)
    builder.button(text='Хочу пройти все бесплатные уроки! ' + emoji.emojize("😋"),
                   callback_data='parent_want_to_be_children')
    builder.adjust(1, 1)
    return builder.as_markup()


def get_inline_teacher_all_block():
    builder = InlineKeyboardBuilder()
    builder.button(text='Стать партнером', callback_data='effeefwwefefe',
                   url=course_referal)
    builder.button(text='Хочу пройти все бесплатные уроки! ' + emoji.emojize("😋"),
                   callback_data='parent_want_to_be_children')
    builder.adjust(1, 1)
    return builder.as_markup()


def get_inline_teacher_all_block_referal():
    builder = InlineKeyboardBuilder()
    builder.button(text='Стать партнером', callback_data='effeefwwefefe',
                   url=course_referal)
    builder.adjust(1, 1)
    return builder.as_markup()


def get_inline_parent_all_block_pay():
    builder = InlineKeyboardBuilder()
    builder.button(text='Оплатить', callback_data='effeefwwefefe',
                   url=course_link)
    builder.adjust(1, 1)
    return builder.as_markup()


def get_inline_test():
    builder = InlineKeyboardBuilder()
    builder.button(text='Готов потренироваться ' + emoji.emojize("😋"), callback_data='want_to_train')
    builder.button(text='Хочу повторить теорию ' + emoji.emojize("😌"), callback_data='back_to_theory')
    builder.adjust(1, 1)
    return builder.as_markup()


def get_inline_is_like():
    builder = InlineKeyboardBuilder()
    builder.button(text='Да ' + emoji.emojize("😋"), callback_data='yes')
    builder.button(text='Нет ' + emoji.emojize("😒"), callback_data='no')
    builder.button(text='Пропустить', callback_data='skip')
    builder.adjust(2, 1)
    return builder.as_markup()


def get_inline_pay():
    builder = InlineKeyboardBuilder()
    builder.button(text='Сслыка', callback_data='effeefwwefefe',
                   url=course_link)
    builder.button(text='Назад', callback_data='back_from_pay')
    return builder.as_markup()


def get_inline_referal():
    builder = InlineKeyboardBuilder()
    builder.button(text='Сслыка', callback_data='effeefwwefe44fe',
                   url=course_referal)
    builder.button(text='Назад', callback_data='back_from_pay')
    return builder.as_markup()


def get_inline_pay_end():
    builder = InlineKeyboardBuilder()
    builder.button(text='Оплата курса', callback_data='effeefwwefefe',
                   url=course_link)
    builder.button(text='Задать вопрос Хэппи', callback_data='effeefww54efefe',
                   url=happy_link)
    builder.adjust(1, 1)
    return builder.as_markup()


def get_inline_support():
    builder = InlineKeyboardBuilder()
    builder.button(text='Задать вопрос Хэппи', callback_data='effeefww54efefe',
                   url=happy_link)
    return builder.as_markup()


def get_inline_next_block():
    builder = InlineKeyboardBuilder()
    builder.button(text='Да 👍', callback_data='next_block_children')
    return builder.as_markup()


def questions_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='По вопросам квеста 🤓',
                   url=happy_link)
    builder.button(text='Не работает бот 🛠',
                   url='https://t.me/mshsor')
    builder.adjust(1, 1)
    return builder.as_markup()


def get_inline_first_video():
    builder = InlineKeyboardBuilder()
    builder.button(text='Хочу пройти квест ' + emoji.emojize("😋"), callback_data='go_to_quest')
    builder.adjust(1, 1)
    return builder.as_markup()


def skip_task_kb(return_callback, callback_data):
    builder = InlineKeyboardBuilder()
    builder.button(text='Да', callback_data=return_callback)
    builder.button(text='Нет', callback_data=callback_data)
    builder.adjust(1, 1)
    return builder.as_markup()
