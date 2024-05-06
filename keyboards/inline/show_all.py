from telebot import types


def get_show_all_button(request: str):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Посмотреть все', callback_data=f'online_show/{request}'))
    return markup


def get_show_all_offline_button(data: str):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(f'Показать все совпадения', callback_data=f'offline_show/{data}'))
    return markup
