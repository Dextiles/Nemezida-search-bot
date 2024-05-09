from bs4 import BeautifulSoup
from config_data import config
from utils.misc import session_creator


class TouchAndParse:
    def __init__(self):
        self.__query_url = 'https://nemez1da.ru/?s='
        self.__unparsed_elems = ['spravochnik', 'rassledovaniya', 'files-vch-3057']
        self.__headers = config.HEADERS
        self.__links = list()

    def __query_creator(self, query: str):
        return self.__query_url + query.replace(' ', '+')

    def get_links(self, url: str):
        url1 = self.__query_creator(url)
        soup = BeautifulSoup(session_creator.get_session().get(url1, headers=self.__headers).text, 'lxml')
        person_links = soup.find_all('h3', {'class': 'simple-grid-grid-post-title'})
        for link in person_links:
            person_link = link.find('a').get('href')
            if not person_link.split('/')[3] in self.__unparsed_elems:
                url = ''.join([i.lower() for i in url if not i.isdigit() and not i == ' '])
                if url in link.text.lower().replace(' ', ''):
                    self.__links.append(person_link)
        return self.__links

    def get_person_data(self, url: str):
        data_frame = dict()
        try:
            soup_object = BeautifulSoup(session_creator.get_session().get(url, headers=self.__headers).text, 'lxml')
            data_frame['ФИО'] = soup_object.title.text.split(" - ")[0]
            for elem in soup_object.find_all('div' and 'b'):
                key, value = elem.parent.find('b').text, elem.parent.text
                data_frame[key] = value.replace(key, '').strip()
            data_frame['Сайт'] = url
        except Exception:
            pass
        else:
            return data_frame
