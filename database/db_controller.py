import sqlalchemy as db
import pandas as pd


class ParsedDataController:
    def __init__(self):
        self.__engine = db.create_engine('sqlite:///database/db.sqlite')


    def search_persons_by_name_and_date(self, text: str):
        params, query = [param.strip() for param in text.split(',')], ''
        if len(params) == 2:
            name, date = params
            query = f"SELECT * FROM data WHERE post_title LIKE '%{name}%' AND data_rozhdeniya LIKE '%{date}%'"
        elif len(params) == 1:
            name = params[0]
            query = f"SELECT * FROM data WHERE post_title LIKE '%{name}%'"
        else:
            return 'ERROR'
        with self.__engine.connect() as conn:
            res = conn.execute(db.text(query))
        return res.fetchall()
