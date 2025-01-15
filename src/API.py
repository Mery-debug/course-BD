import requests
import os
from dotenv import load_dotenv


class APIhh:
    def __init__(self, word):
        self.word: str = word
        self.params = {}
        self.headers = {'text': ''}
        self.company = []

    def search_api_hh_clients(self, company=None):
        if company is None:
            company = [{}]
        url = "https://api.hh.ru/employers/"
        load_dotenv()
        for name in os.getenv('lst'):
            self.params = {'sort_by': 'by_vacancies_open', 'text': name, 'page': 0, 'per_page': 10,
                           'only_with_vacancies': 'only_with_vacancies'}
            while self.params.get('page') != 10:
                r = requests.get(url, headers=self.headers, params=self.params)
                if r.status_code == 200:
                    company = r.json()['items']
                    self.company.extend(company)
                    self.params['page'] += 1
                    return f"id {[com.get('id') for com in company]}, \nname {[com.get('name') for com in company]}, " \
                           f"\nopen_vacancies {[com.get('open_vacancies') for com in company]}"
                else:
                    return f'Возможная причина {r.reason}'


p = APIhh('python').search_api_hh_clients()
print(p)
