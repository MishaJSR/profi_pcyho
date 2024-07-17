from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline(callback_data):
    builder = InlineKeyboardBuilder()
    builder.button(text='Пройти задание по курсу', callback_data=callback_data)
    return builder.as_markup()

def get_inline_vebinar(url):
    builder = InlineKeyboardBuilder()
    builder.button(text='Перейти на вебинар', callback_data='asdsaafafadasdasdafaac',
                   url=url)
    return builder.as_markup()
