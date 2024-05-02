import json
from bs4 import BeautifulSoup
from utils.misc.parser_utils import session_creator, transliterate, parser_timer
import pandas as pd
import numpy as np
from threading import Thread
from typing import NoReturn
from config_data import config
from database import db_controller
import sqlalchemy
import os
from datetime import datetime


class LinksGetter:

    def __init__(self):
        self.__start_data = super().__init__()
        self.__headers = config.HEADERS
        self.__parser_blocks = 10
        self.__start_urls = ["https://nemez1da.ru/voennoplennye/",
                             "https://nemez1da.ru/voennye-prestupniki/",
                             "https://nemez1da.ru/naczistskie-podrazdeleniya/",
                             "https://nemez1da.ru/posobniki/",
                             "https://nemez1da.ru/inostrannye-posobniki-i-naemniki/",
                             "https://nemez1da.ru/posobniki/network-terrorists/"]
        self.__all_links = list()

    def __get_links(self, url):
        soup_object = BeautifulSoup(session_creator.get_session().get(url, headers=self.__headers).text, 'lxml')
        person_links = soup_object.find_all('h3', {'class': 'simple-grid-grid-post-title'})
        links = [elem.find('a').get('href') for elem in person_links]
        self.__all_links.extend(links)
        print(links)
        try:
            next_page = soup_object.find('a', {'class': 'next page-numbers'}).get('href')
        except AttributeError:
            return
        else:
            self.__get_links(next_page)

    def get_all(self):
        for url in self.__start_urls:
            self.__get_links(url)
        print('Найдено всего: ', len(self.__all_links))
        return self.__all_links


class Parser:
    def __init__(self):
        self.__headers = config.HEADERS
        self.__controller = db_controller.ParsedDataController()

    def __get_person_data(self, url: str) -> dict or bool:
        data_frame, links = dict(), list()
        try:
            soup_object = BeautifulSoup(session_creator.get_session().get(url, headers=self.__headers).text, 'lxml')
            data_frame['full_name'] = [soup_object.title.text.split(" - ")[0]]
            other_info = dict()
            for elem in soup_object.find_all('div' and 'b'):
                key, value = elem.parent.find('b').text, elem.parent.text
                if key == 'Дата рождения':
                    data_frame['date_of_Birth'] = [value.replace(key, '').strip()]
                else:
                    other_info[key] = [value.replace(key, '').strip()]
            data_frame['link'] = [url]
            data_frame['other_info'] = [json.dumps(other_info, ensure_ascii=False)]
            for link in soup_object.find_all('a'):
                actual = link.get('href')
                if str(actual).endswith('.jpg'):
                    links.append(str(actual))
        except Exception:
            pass
        else:
            return pd.DataFrame.from_dict(data_frame)

    @parser_timer.timer
    def parse(self):
        controller = db_controller.ParsedDataController()
        links = LinksGetter().get_all()
        total_values, success_parsed = len(links), 0
        for i, link in enumerate(links):
            try:
                new_person = self.__get_person_data(link)
                controller.save_parsed_data(new_person)
            except Exception:
                pass
            else:
                success_parsed += 1
        controller.save_parsed_metadata(pd.DataFrame.from_dict(
            {'parser_datetime': [datetime.strftime(datetime.now(), config.DATE_FORMAT_FULL)],
             'total_values': [total_values],
             'success_parsed': [success_parsed]}))
