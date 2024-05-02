import sqlalchemy as db
import pandas as pd


class ParsedDataController:
    def __init__(self):
        self.__engine = db.create_engine('sqlite:///database/parsed_data/data.sql')
        self.__conn = self.__engine.connect()
        self.__metadata = db.MetaData()

    def save_parsed_data(self, data: pd.DataFrame):
        data.to_sql('persons', con=self.__conn, if_exists='append', index=False)

    def save_parsed_metadata(self, data: pd.DataFrame):
        data.to_sql('metadata', con=self.__conn, if_exists='replace', index=False)
