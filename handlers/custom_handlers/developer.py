from telebot.types import Message # noqa
from keyboards.inline import about_developer
from loader import bot
from typing import NoReturn


@bot.message_handler(commands=["developer"])
def about_me(message: Message) -> NoReturn:
    bot.send_message(message.chat.id, '\U0001F464 Разработчик сервиса: Иван Пермяков\n'
                                      'Основной директ, сотрудничество: @Dextiles\n\n',
                     reply_markup=about_developer.get_about_developer_markup())
