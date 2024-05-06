from telebot import types


def get_db_button():
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Получить копию БД', callback_data=f'get_db'))
    return markup
