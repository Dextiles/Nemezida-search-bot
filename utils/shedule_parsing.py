import schedule
from parser.Nemez1da_parser import Parser
import time
from config_data.config import PARSER_OPTIONS


def start_schedule():
    schedule.every(PARSER_OPTIONS.update_frequency).days.at(PARSER_OPTIONS.parsing_time).do(Parser().parse())
    while True:
        schedule.run_pending()
        time.sleep(1)
