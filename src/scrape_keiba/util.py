import logging
from time import sleep

import requests
from bs4 import BeautifulSoup

SLEEP = 3
TIMEOUT = 60000


def get_soup(url: str) -> BeautifulSoup:
    logging.info(f"request url: {url}")
    sleep(SLEEP)
    response: requests.Response = requests.get(url=url, timeout=TIMEOUT)
    return BeautifulSoup(
        markup=response.content,
        features="lxml",
        from_encoding="EUC-JP",
    )
