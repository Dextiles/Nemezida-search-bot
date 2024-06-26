import os
from dotenv import load_dotenv, find_dotenv
from utils.misc import parser_properties
import logging

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

if not os.path.exists('logs'):
    os.mkdir('logs')

BOT_TOKEN = os.getenv("BOT_TOKEN")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DATE_FORMAT_FULL = '%Y-%m-%d %H:%M:%S'
INSTRUCTION_URL = "https://dextiles.github.io/Dextiles-instructions/nemezida-search-bot"
HOME_PAGE = 'https://nemez1da.ru/'
PARSER_OPTIONS = parser_properties.ParserOptions()
BOT_VERSION = '0.02-alfa'
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("info", "Информация о базе данных"),
    ("developer", "Информация о разработчике"),
)

ONLINE_MESS = '\U0001F7E2 (Сетевой)\n\n'
OFFLINE_MESS = '\U0001F534 (Автономный)\n\n'

logging.basicConfig(level=logging.INFO, filename='logs/usage.log', filemode='w', encoding='utf-8',
                    format='%(asctime)s %(levelname)s %(message)s', datefmt=DATE_FORMAT_FULL)
