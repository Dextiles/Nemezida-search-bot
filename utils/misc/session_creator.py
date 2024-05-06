from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
from config_data.config import HOME_PAGE, HEADERS


def get_session() -> requests.Session:
    """
    Function to get a requests Session object with custom retry settings.
    Returns:
        requests.Session: A Session object with custom retry settings.
    """
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def try_connection() -> bool:
    if requests.get(HOME_PAGE, headers=HEADERS).status_code == 200:
        return True
    else:
        return False
