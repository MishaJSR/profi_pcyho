from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline(callback_data):
    builder = InlineKeyboardBuilder()
    builder.button(text='Пройти задание', callback_data=callback_data)
    return builder.as_markup()

def get_inline_vebinar(url):
    builder = InlineKeyboardBuilder()
    builder.button(text='Перейти на вебинар', callback_data='asdsaafafadasdasdafaac',
                   url=url)
    return builder.as_markup()


def get_inline_parent():
    builder = InlineKeyboardBuilder()
    builder.button(text='Перейти к регистрации', callback_data='asdsaafafadasdasdafaac')
    return builder.as_markup()

def get_inline_parent_all_block():
    builder = InlineKeyboardBuilder()
    builder.button(text='Вперед!', callback_data='parent_want_to_be_children')
    return builder.as_markup()