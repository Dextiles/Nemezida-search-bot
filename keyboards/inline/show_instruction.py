from telebot import types
import validators
from config_data.config import INSTRUCTION_URL


def get_show_instruction_button():
    try:
        if not validators.url(INSTRUCTION_URL):
            raise ValueError
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton('Инструкция',
                                              web_app=types.WebAppInfo(url=INSTRUCTION_URL)))
        return markup
    except ValueError:
        return types.ReplyKeyboardRemove()
