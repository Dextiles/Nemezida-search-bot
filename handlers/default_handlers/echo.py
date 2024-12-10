from telebot.types import Message
from loader import bot
from parser import touch_and_parse, file_checker
from utils.misc import message_creator
from keyboards.inline import show_more as btn
from keyboards.inline import show_all as show_all_btn
from keyboards.inline import show_instruction as show_instruction_btn
from utils.misc import session_creator
from database.db_controller import ParsedDataController as ControllerData
from config_data.config import OFFLINE_MESS, ONLINE_MESS
from uuid import uuid1
import os
import shutil


@bot.message_handler(state=None)
def bot_echo(message: Message):
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
            result = ControllerData().search_persons_by_name_and_date(message.text)
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
    results = ControllerData().search_persons_by_name_and_date(call.data.split('/')[1])
    length = len(results)
    for i, result in enumerate(results, start=1):
        bot.reply_to(call.message, f'{OFFLINE_MESS}'
                                   f'Совпадение {i} из {length}\n\n'
                                   f'<b>ФИО:</b> {result[0]}\n\n'
                                   f'<b>Дата рождения:</b> {result[1]}\n\n'
                                   f'<b>Категория:</b> {result[2]}\n\n',
                     parse_mode='HTML')


@bot.message_handler(content_types=['document'])
def package_search(message: Message):
    try:
        file_info = bot.get_file(message.document.file_id)
        if not file_info.file_path.split('.')[1].lower() == 'csv':
            raise ValueError('\U0000274c Такой формат не поддерживается! Только *.csv!')
        else:
            bot.reply_to(message, '\U0001f300 Пожалуйста ждите, выполняю анализ...')
            uid = uuid1()
            directory = f'working_directory/{uid}'
            downloaded_file = bot.download_file(file_info.file_path)
            os.mkdir(directory)
            src = f'{directory}/{message.document.file_name}'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            result = file_checker.PackageSearch(uid, src).check()

            if not result['error']:
                if result['matched'] == 0:
                    bot.send_message(message.chat.id,
                                     f'Обработано элементов: <b>{result["total"]}</b>\n'
                                     f'\U0000203C <b>Совпадений не найдено!</b>',
                                     parse_mode='HTML')
                else:
                    with open(result['path'], 'rb') as ready_file:
                        bot.send_document(message.chat.id,
                                          ready_file,
                                          caption=f'Обработано элементов: <b>{result["total"]}</b>\n'
                                                  f'\U0000203C Найдено совпадений: <b>{result["matched"]}</b>\n'
                                                  f'Отчет сформирован!',
                                          parse_mode='HTML')
            else:
                raise ValueError(result['error'])

            shutil.rmtree(f'working_directory/{uid}')

    except Exception as ex:
        bot.reply_to(message, f'Упс..., что-то пошло не так:\n'
                              f'{ex}')
