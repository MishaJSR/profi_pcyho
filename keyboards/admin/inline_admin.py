import emoji
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline(callback_data):
    builder = InlineKeyboardBuilder()
    builder.button(text='Да, мне всё понятно ' + emoji.emojize('🤗'), callback_data=callback_data)
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
    builder.button(text='Оплатить', callback_data='pay')
    builder.button(text='Хочу пройти все бесплатные уроки! ' + emoji.emojize("😋"), callback_data='parent_want_to_be_children')
    builder.adjust(1, 1)
    return builder.as_markup()


def get_inline_parent_all_block_pay():
    builder = InlineKeyboardBuilder()
    builder.button(text='Оплатить', callback_data='pay')
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
                   url="https://www.google.ru/")
    builder.button(text='Назад', callback_data='back_from_pay')
    return builder.as_markup()