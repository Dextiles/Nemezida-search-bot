from telebot.types import Message # noqa
from loader import bot
from database.db_controller import ParsedDataController as Controller


@bot.message_handler(commands=["info"])
def bot_start(message: Message):
    metadata = Controller().get_metadata()
    bot.reply_to(message, f'<b>Дата обновления БД:</b>\n{metadata[0][0].replace('-', '.')}\n'
                          f'<b>Всего записей в БД</b>: {metadata[0][2]}\n'
                          f'<b>Всего записей на сайте</b>: {metadata[0][1]}',
                 parse_mode='HTML')
