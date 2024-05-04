from telebot import types # noqa


def get_about_developer_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('vk', url='https://vk.com/dextiles'),
               types.InlineKeyboardButton('instagram', url='https://www.instagram.com/jack_danie1s'))
    markup.row(types.InlineKeyboardButton('github', url='https://github.com/Dextiles'))
    return markup
