from telebot import types


def get_show_all_results_button(data: str):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(f'Показать все совпадения', callback_data=f'show_all/{data}'))
    return markup


def get_more_info_button(link: str):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton(f'Подробнее', web_app=types.WebAppInfo(url=link)))
    return markup
