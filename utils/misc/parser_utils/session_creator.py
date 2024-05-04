from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests


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
