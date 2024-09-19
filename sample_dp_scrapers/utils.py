from bs4 import BeautifulSoup


import requests


def get_soup(url: str) -> BeautifulSoup:
    response: requests.Response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")
