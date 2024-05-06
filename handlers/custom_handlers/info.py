from telebot.types import Message # noqa
from loader import bot
from database.db_controller import ParsedDataController as Controller
from keyboards.inline import send_db


@bot.message_handler(commands=["info"])
def bot_start(message: Message):
    metadata = Controller().get_metadata()
    bot.reply_to(message, f'<b>Локальная база данных</b>\n\n'
                          f'<b>Дата обновления:</b>\n{metadata[0][0].replace("-", ".")}\n'
                          f'<b>Всего записей:</b> {metadata[0][2]}\n'
                          f'<b>Всего записей на сайте:</b> {metadata[0][1]}',
                 reply_markup=send_db.get_db_button(),
                 parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data == 'get_db')
def get_db(call):
    invoke = bot.reply_to(call.message, 'Ждите, отправляю базу данных...')
    with open('database/parsed_data/parsed_data.sql', 'rb') as file:
        bot.send_document(call.message.chat.id, file, caption='База данных')
    bot.delete_message(call.message.chat.id, invoke.message_id)
