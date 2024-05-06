import sqlalchemy as db
import pandas as pd


class ParsedDataController:
    def __init__(self):
        self.__engine = db.create_engine('sqlite:///database/parsed_data/parsed_data.sql')

    def save_parsed_data(self, data: pd.DataFrame):
        with self.__engine.connect() as conn:
            data.to_sql('persons', con=conn, if_exists='replace', index=False)

    def save_parsed_metadata(self, data: pd.DataFrame):
        with self.__engine.connect() as conn:
            data.to_sql('metadata', con=conn, if_exists='replace', index=False)

    def search_persons_by_name_and_date(self, text: str):
        params, query = [param.strip() for param in text.split(',')], ''
        if len(params) == 2:
            name, date = params
            query = f"SELECT * FROM persons WHERE full_name LIKE '%{name}%' AND date_of_birth LIKE '%{date}%'"
        elif len(params) == 1:
            name = params[0]
            query = f"SELECT * FROM persons WHERE full_name LIKE '%{name}%'"
        else:
            return 'ERROR'
        with self.__engine.connect() as conn:
            res = conn.execute(db.text(query))
            return res.fetchall()

    def get_metadata(self):
        with self.__engine.connect() as conn:
            res = conn.execute(db.text("SELECT * FROM metadata"))
            return res.fetchall()
