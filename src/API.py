import requests
import os
from dotenv import load_dotenv


class APIhh:
    def __init__(self, word):
        self.word: str = word
        load_dotenv()
        for name in os.getenv('lst'):
            self.params = {'text': name, 'page': 0, 'per_page': 100, 'only_with_vacancies': 'only_with_vacancies'}
        self.headers = {'name': ''}
        self.company = []

    def search_api_hh_clients(self):
        company = [{}]
        url = "https://api.hh.ru/employers"
        while self.params.get('page') != 50:
            r = requests.get(url, headers=self.headers, params=self.params)
            if r.status_code == 200:
                company = r.json()['items']
                self.company.extend(company)
                self.params['page'] += 1
            else:
                return f'Возможная причина {r.reason}'
        # return company
        return f"id {[com.get('id') for com in company]}, \nname {[com.get('name') for com in company]}, " \
               f"\nopen_vacancies {[com.get('open_vacancies') for com in company]}"


p = APIhh('python').search_api_hh_clients()
print(p)
