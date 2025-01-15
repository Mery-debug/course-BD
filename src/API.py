import requests
import os
from dotenv import load_dotenv
from beautifultable import BeautifulTable


class APIhh:
    def __init__(self, word):
        self.word: str = word
        self.params = {}
        self.headers = {'text': ''}
        self.company = []
        self.vacancies = []

    def search_api_hh_clients(self, company=None):
        """Метод для работы с апи и получении информации о работодателях"""
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
                    return company
                else:
                    return f'Возможная причина {r.reason}'

    def search_api_vacancies(self, company):
        """
        Поиск вакансий для найденных компаний,
        только 20 вакансий для каждой компании,
        чтобы не перегружать таблицы
        """
        vacancie = [{}]
        vacan = []
        url = "https://api.hh.ru/vacancies"
        com = [com['id'] for com in company]
        self.params = {'text': self.word, 'employer_id': com, 'page': 0, 'per_page': 100}
        while self.params.get('page') != 20:
            r = requests.get(url, params=self.params)
            if r.status_code == 200:
                vacancies = r.json()['items']
                self.vacancies.extend(company)
                self.params['page'] += 1
                for vac in vacancies:
                    vacan = [
                        {
                            'vacancie_id': vac['id'],
                            'name': vac['name'],
                            'salary': vac['salary'],
                            'url': vac['url'],
                            'employer_id': vac['employer']['id']
                        }
                    ]
                    vacancie.append(vacan)
        return vacancie


def expectation_table_employees(compani):
    """ Функция для красивого отображения результатов поиска в таблице о работодателях"""
    table = BeautifulTable()
    table.column_headers = ["id", "company", "url", "open vacancies"]
    for com in compani:
        table.append_row([com['id'], com['name'], com['url'], com['open_vacancies']])
    return table


p = APIhh('python').search_api_hh_clients()
print(expectation_table_employees(compani=p))
v = APIhh('python').search_api_vacancies(company=p)
print(v)

