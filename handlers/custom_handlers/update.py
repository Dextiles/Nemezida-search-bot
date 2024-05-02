from telebot.types import Message # noqa
from loader import bot
from parser import Nemez1da_parser as parser_instrument
from threading import Thread


@bot.message_handler(commands=["update"])
def bot_start(message: Message):
    bot.send_message(message.chat.id, 'Запущено принудительное обновление базы данных...')
    Thread(target=parser_instrument.Parser().parse).start()
