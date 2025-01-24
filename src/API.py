import os

import requests
from dotenv import load_dotenv


class APIhh:
    def __init__(self, word):
        self.word: str = word
        self.params = {}
        self.headers = {"text": ""}
        self.company = []
        self.vacancies = []

    def search_api_hh_clients(self, company: list[dict] = None) -> list[dict]:
        """Метод для работы с апи и получении информации о работодателях"""
        if company is None:
            company = []
        compan = {}
        url = "https://api.hh.ru/employers/"
        load_dotenv()
        for name in os.getenv("lst"):
            self.params = {
                "sort_by": "by_vacancies_open",
                "text": name,
                "page": 0,
                "per_page": 10,
                "only_with_vacancies": "only_with_vacancies",
            }
            while self.params.get("page") != 10:
                r = requests.get(url, headers=self.headers, params=self.params)
                if r.status_code == 200:
                    for com in r.json()["items"]:
                        compan = {
                            "id": int(com["id"]),
                            "name": com["name"],
                            "url": com["url"],
                            "open_vacancies": com["open_vacancies"],
                        }
                        company.append(compan)
                    self.company.extend(company)
                    self.params["page"] += 1
                    return company

    def search_api_vacancies(self, company: list[dict]) -> list[dict]:
        """
        Поиск вакансий для найденных компаний
        """
        vacancie = []
        vacan = {}
        url = "https://api.hh.ru/vacancies"
        co = [com.get("id") for com in company]
        self.params = {"text": self.word, "employer_id": co, "page": 0, "per_page": 100}
        while self.params.get("page") != 20:
            r = requests.get(url, params=self.params)
            if r.status_code == 200:
                vacancies = r.json()["items"]
                self.vacancies.extend(company)
                self.params["page"] += 1
                for vac in vacancies:
                    if vac["salary"] and vac["salary"]["currency"] == "RUR":
                        vacan = {
                            "vacancie_id": vac["id"],
                            "name": vac["name"],
                            "salary": vac["salary"],
                            "url": vac["url"],
                            "employer_id": vac["employer"]["id"],
                        }
                        vacancie.append(vacan)
            return vacancie


# p = APIhh('python').search_api_hh_clients()
# print(p)
# v = APIhh('python').search_api_vacancies(company=p)
# print(v)
