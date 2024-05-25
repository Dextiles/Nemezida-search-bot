from telebot.types import Message
from loader import bot
from parser import touch_and_parse
from utils.misc import message_creator
from keyboards.inline import show_more as btn
from keyboards.inline import show_all as show_all_btn
from keyboards.inline import show_instruction as show_instruction_btn
from utils.misc import session_creator
from database.db_controller import ParsedDataController as PDC
from config_data.config import OFFLINE_MESS, ONLINE_MESS
import logging


@bot.message_handler(state=None)
def bot_echo(message: Message):
    logging.info(f'id{message.from_user.id} запрос: "{message.text}"')
    if set(".:;!_*-+()/#¤%&)").isdisjoint(message.text):
        if session_creator.try_connection():
            message.text = message.text.replace(',', '')
            parser = touch_and_parse.TouchAndParse()
            links = parser.get_links(message.text)
            length = len(links)
            if length == 1:
                data = parser.get_person_data(links[0])
                bot.reply_to(message, f'{ONLINE_MESS}'
                                      f'{message_creator.get_info_message(data)}',
                             parse_mode='HTML',
                             reply_markup=btn.get_show_more_button(data['Сайт']))
            elif 1 < length < 15:
                bot.reply_to(message, f'{ONLINE_MESS}'
                                      f'По вашему запросу найдено несколько совпадений ({length})\n'
                                      f'Хотите просмотреть все?',
                             reply_markup=show_all_btn.get_show_all_button(message.text))
            elif length == 0:
                bot.reply_to(message, f'{ONLINE_MESS}По вашему запросу ничего не найдено')
            else:
                bot.reply_to(message, f'{ONLINE_MESS}Слишком много результатов ({length}), уточните запрос')
        else:
            result = PDC().search_persons_by_name_and_date(message.text)
            length = len(result)
            if result == 'ERROR' or length == 0:
                bot.reply_to(message, f'{OFFLINE_MESS}По вашему запросу нет совпадений, либо неверный запрос!')
            if length > 15:
                bot.reply_to(message, f'{OFFLINE_MESS}По вашему запросу найдено очень много совпадений'
                                      f' ({length}), уточните запрос!')
            else:
                if length == 1:
                    bot.reply_to(message, f'{OFFLINE_MESS}'
                                          f'Есть совпадение!\n\n'
                                          f'<b>ФИО:</b> {result[0][0]}\n\n'
                                          f'<b>Дата рождения:</b> {result[0][1]}\n\n'
                                          f'<b>Категория:</b> {result[0][2]}\n\n',
                                 reply_markup=btn.get_show_more_button_offline(),
                                 parse_mode='HTML')
                elif length > 1:
                    bot.reply_to(message, f'{OFFLINE_MESS}Обнаружено несколько совпадений: {length}!',
                                 reply_markup=show_all_btn.get_show_all_offline_button(message.text))
    else:
        bot.reply_to(message, 'В запросах нельзя использовать специальные символы!\n'
                              'Пожалуйста, изучите инструкцию!',
                     reply_markup=show_instruction_btn.get_show_instruction_button())


@bot.callback_query_handler(func=lambda call: call.data.startswith('online_show'))
def show_all(call):
    request = call.data.split('/')[1]
    parser = touch_and_parse.TouchAndParse()
    links = parser.get_links(request)
    length = len(links)
    for i, link in enumerate(links, start=1):
        data = parser.get_person_data(link)
        bot.reply_to(call.message, f'{ONLINE_MESS}'
                                   f'Совпадение {i} из {length}\n\n'
                                   f'{message_creator.get_info_message(data)}',
                     parse_mode='HTML',
                     reply_markup=btn.get_show_more_button(data['Сайт']))


@bot.callback_query_handler(func=lambda call: call.data.startswith('offline_show'))
def show_all_offline(call):
    results = PDC().search_persons_by_name_and_date(call.data.split('/')[1])
    length = len(results)
    for i, result in enumerate(results, start=1):
        bot.reply_to(call.message, f'{OFFLINE_MESS}'
                                   f'Совпадение {i} из {length}\n\n'
                                   f'<b>ФИО:</b> {result[0]}\n\n'
                                   f'<b>Дата рождения:</b> {result[1]}\n\n'
                                   f'<b>Категория:</b> {result[2]}\n\n',
                     parse_mode='HTML')
