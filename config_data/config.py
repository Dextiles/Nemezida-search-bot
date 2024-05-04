import os
from dotenv import load_dotenv, find_dotenv
from utils import parser_properties

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PARSER_OPTIONS = parser_properties.ParserOptions()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'}
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DATE_FORMAT_FULL = '%Y-%m-%d %H:%M:%S'
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("info", "Посмотреть информацию о боте и БД"),
    ("developer", "Информация о разработчике"),
)
