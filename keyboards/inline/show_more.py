from telebot import types


def get_show_more_button(url: str):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('Еще', web_app=types.WebAppInfo(url=url)))
    return markup
