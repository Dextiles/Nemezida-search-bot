import sqlalchemy as db
import pandas as pd
import openpyxl
import uuid
import time


class PackageSearch:
    def __init__(self, uid: uuid, file_path: str) -> None:
        self._uid = uid
        self._file_path = file_path
        self._db_engine = db.create_engine('sqlite:///database/db.sqlite')

    def check(self) -> dict[str: str] | dict[str: None]:
        matched = list()
        try:
            persons_to_check = pd.read_csv(self._file_path, encoding='cp1251')
            with self._db_engine.connect() as conn:
                for person_string_element in persons_to_check.to_numpy():
                    data_simpled: list[str] = person_string_element[0].split(';')
                    if not len(data_simpled) == 4:
                        raise ValueError('Ошибка в формате пакета!')
                    date_of_birth: str = data_simpled.pop(3)
                    try:
                        time.strptime(date_of_birth, '%d.%m.%Y')
                    except ValueError:
                        return {'error': 'В списке есть невалидная дата, проверьте!'}
                    data_component: str = ' '.join(data_simpled).strip().lower().title()
                    result = self.__string_searcher(conn, data_component, date_of_birth)
                    if result:
                        matched.extend(result)
            return self.__report_generator(matched, len(persons_to_check))
        except Exception as ex:
            return {'error': ex}

    @staticmethod
    def __string_searcher(connection, component: str, date_of_birth: str) -> list:
        query = (f'SELECT category, '
                 f'post_title, '
                 f'data_rozhdeniya, '
                 f'prozhivaet_po_adresu, '
                 f'telefon, telegram, '
                 f'pochta, vkontakte, '
                 f'fejsbuk,'
                 f'image, '
                 f'tvitter, '
                 f'odnoklassniki, '
                 f'instagram, '
                 f'deyatelnost, '
                 f'komprometiruyushhij_material, '
                 f'kategoriya, '
                 f'dolzhnost, '
                 f'zvanie, '
                 f'dopolnitelno '
                 f'from data WHERE post_title LIKE "%{component}%" AND data_rozhdeniya LIKE "{date_of_birth}"')
        return connection.execute(db.text(query)).fetchall()

    def __report_generator(self, matched_elements: list, total_len: int):
        if not matched_elements:
            return {'error': None, 'matched': 0, 'total': total_len}
        else:
            file_name = self._file_path.split('/')[-1].split('.')[0]
            path_to_report = f'working_directory/{self._uid}/{file_name}.xlsx'
            openpyxl.Workbook().save(path_to_report)
            df = pd.DataFrame(matched_elements)
            ready_df = df.rename(columns={'category': 'Категория',
                                          'post_title': 'ФИО',
                                          'data_rozhdeniya': 'Дата рождения',
                                          'prozhivaet_po_adresu': 'Адрес проживания',
                                          'telefon': 'Телефон',
                                          'telegram': 'Телега',
                                          'pochta': 'Почта',
                                          'vkontakte': 'Вконтакте',
                                          'fejsbuk': 'Facebook',
                                          'image': 'Фото',
                                          'tvitter': 'Твиттер',
                                          'odnoklassniki': 'Одноклассники',
                                          'instagram': 'Instagram',
                                          'deyatelnost': 'Деятельность',
                                          'komprometiruyushhij_material': 'Компромат',
                                          'kategoriya': 'Категория',
                                          'dolzhnost': 'Должность',
                                          'zvanie': 'Звание',
                                          'dopolnitelno': 'Дополнительно'})
            ready_df.to_excel(path_to_report, index=False, header=True)
            return {'error': None, 'matched': len(matched_elements), 'total': total_len, 'path': path_to_report}
