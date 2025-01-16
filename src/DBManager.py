import os
from typing import Any

import psycopg2
from dotenv import load_dotenv


def create_database(**params: dict):
    """
    Создание базы данных для хранения информации о работодателях и их вакансиях
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    load_dotenv()
    db_name = os.getenv('database')

    cur.execute(f"DROP DATABASE IF EXIST {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()

    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE company (
                id SERIAL PRIMARY KEY,
                company VARCHAR(255) NOT NULL,
                url TEXT NOT NULL,
                open_vacancies INTEGER
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                salary from INT,
                salary to INT,
                vacancies_url TEXT,
                employer_id INT REFERENCES company(id)
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(company: list[dict], vacancy: list[dict], **params: dict):
    """
    Сохранение данных о компаниях и вакансиях в базу данных
    """
    load_dotenv()
    db_name = os.getenv("dbname")
    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        for com in company:
            company_id = com['id']
            company_url = com['url']
            company_name = com['name']
            company_open_vacancies = com['open_vacancies']
            cur.execute(
                """
                INSERT INTO company (id, name, url, open_vacancies)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (company_id, company_name, company_url, company_open_vacancies)
            )
            company_id = cur.fetchone()[0]
            employer_id = company_id
            for vac in vacancy:
                vacancy_id = vac['vacancie_id']
                vacancy_name = vac['name']
                vacancy_sal_from = vac['salary']['from']
                vacancy_sal_to = vac['salary']['to']
                vacancy_url = vac['url']
                vacancy_employer_id = vac['employer_id']
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancies_id, name, salary from, salary to, vacancies_url, employer_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (vacancy_id, vacancy_name, vacancy_sal_from, vacancy_sal_to, vacancy_url, vacancy_employer_id)
                )

    conn.commit()
    conn.close()


class DBManager:
    """Класс для работы в базе данных с вакансиями и компаниями"""
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("host"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password")
        )

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """


    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        pass

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям
        """
        pass

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        pass

    def get_vacancies_with_keyword(self):
        """
        Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python
        """
        pass
