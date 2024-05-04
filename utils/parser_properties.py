import json


class ParserOptions:
    def __init__(self):
        try:
            with open('parser_properties.json', 'r') as file:
                self.__options = json.load(file)
        except FileNotFoundError:
            exit('parser_properties.json not found')

    @property
    def update_frequency(self):
        return self.__options['update_frequency']

    @property
    def parsing_time(self):
        return self.__options['parsing_time']

    @property
    def start_endpoints(self):
        return self.__options['start_endpoints']
