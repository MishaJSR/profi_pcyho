from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline():
    builder = InlineKeyboardBuilder()
    builder.button(text='Пройти задание по курсу', callback_data='ss')
    return builder.as_markup()
