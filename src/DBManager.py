import os
import psycopg2
from dotenv import load_dotenv


class DBManager:
    """Класс для работы в базе данных с вакансиями и компаниями"""
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("host"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password")
        )

    def create_database(self, **params: dict):
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
