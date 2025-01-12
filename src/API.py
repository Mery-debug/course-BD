import requests
from src.user_utils import user_params

search = user_params()


class APIhh:
    def __init__(self, word):
        self.word: str = search

    @staticmethod
    def search_api_hh_clients(self, word):
        url = "https://api.hh.ru/employers"
        params = {'text': word, }

        r = requests.get(url, headers=headers, params=params)
        if r == 200:


