from telebot.types import Message
from database.db_controller import ParsedDataController as PDC
from loader import bot
from keyboards.inline import show_all_results


@bot.message_handler(state=None)
def bot_echo(message: Message):
    result = PDC().search_persons_by_name_and_date(message.text)
    length = len(result)
    if result == 'ERROR' or length == 0:
        bot.reply_to(message, 'По вашему запросу нет совпадений, либо неверный запрос!')
    if length > 15:
        bot.reply_to(message, f'По вашему запросу найдено очень много совпадений ({length}), уточните запрос!')
    else:
        if length == 1:
            bot.reply_to(message, f'Есть совпадение!\n\n'
                                  f'<b>ФИО:</b> {result[0][0]}\n'
                                  f'<b>Дата рождения:</b> {result[0][1]}\n'
                                  f'<b>Категория:</b> {result[0][2]}\n',
                         reply_markup=show_all_results.get_more_info_button(result[0][3]),
                         parse_mode='HTML')
        elif length > 1:
            bot.reply_to(message, f'Обнаружено несколько совпадений: {length}!',
                         reply_markup=show_all_results.get_show_all_results_button(message.text))


@bot.callback_query_handler(func=lambda call: call.data.startswith('show_all'))
def show_all_callback(call):
    results = PDC().search_persons_by_name_and_date(call.data.split('/')[1])
    length = len(results)
    for i, result in enumerate(results, start=1):
        bot.reply_to(call.message, f'Совпадение {i} из {length}\n\n'
                                   f'<b>ФИО:</b> {result[0]}\n'
                                   f'<b>Дата рождения:</b> {result[1]}\n'
                                   f'<b>Категория:</b> {result[2]}\n',
                     reply_markup=show_all_results.get_more_info_button(result[3]),
                     parse_mode='HTML')
