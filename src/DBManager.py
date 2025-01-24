import os
from typing import Any

import psycopg2
from dotenv import load_dotenv


def create_database() -> str:
    """
    Создание базы данных для хранения информации о работодателях и их вакансиях
    """
    load_dotenv()
    conn = psycopg2.connect(
        db_name=os.getenv("dbname"),
        database="api_db",
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
    )
    conn.autocommit = True
    cur = conn.cursor()

    load_dotenv()
    db_name = os.getenv("dbname")

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")
    conn.commit()
    conn.close()

    conn = psycopg2.connect(
        host=os.getenv("host"),
        database="api_db",
        user=os.getenv("user"),
        password=os.getenv("password"),
    )
    with conn.cursor() as cur:
        cur.execute(
            """
            DROP TABLE IF EXISTS company CASCADE;
            CREATE TABLE company (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url TEXT NOT NULL,
                open_vacancies INTEGER
            )
        """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
            DROP TABLE IF EXISTS vacancies;
            CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                salary_from INT,
                salary_to INT,
                vacancies_url TEXT,
                employer_id INT REFERENCES company(id)
            )
        """
        )

    conn.commit()
    conn.close()
    return "База данных создана"


def save_data_to_database(company: list[dict], vacancy: list[dict]) -> str:
    """
    Сохранение данных о компаниях и вакансиях в базу данных
    """
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv("host"),
        database="api_db",
        user=os.getenv("user"),
        password=os.getenv("password"),
    )

    with conn.cursor() as cur:
        for com in company:
            company_id = com.get("id")
            company_url = com.get("url")
            company_name = com.get("name")
            company_open_vacancies = com.get("open_vacancies")
            cur.execute(
                """
                INSERT INTO company (id, name, url, open_vacancies)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    str(company_id),
                    str(company_name),
                    str(company_url),
                    int(company_open_vacancies),
                ),
            )
        for vac in vacancy:
            vacancy_id = vac.get("vacancie_id")
            vacancy_name = vac.get("name")
            vacancy_sal_from = vac.get("salary").get("from")
            vacancy_sal_to = vac.get("salary").get("to")
            vacancy_url = vac.get("url")
            vacancy_employer_id = vac.get("employer_id")
            if vacancy_sal_from and vacancy_sal_to:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancies_id, name, salary_from, salary_to, vacancies_url, employer_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        int(vacancy_id),
                        str(vacancy_name),
                        int(vacancy_sal_from),
                        int(vacancy_sal_to),
                        str(vacancy_url),
                        str(vacancy_employer_id),
                    ),
                )
            elif not vacancy_sal_to:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancies_id, name, salary_from, salary_to, vacancies_url, employer_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        str(vacancy_id),
                        str(vacancy_name),
                        str(vacancy_sal_from),
                        0,
                        str(vacancy_url),
                        str(vacancy_employer_id)
                    ),
                )
            elif not vacancy_sal_from:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancies_id, name, salary_from, salary_to, vacancies_url, employer_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        int(vacancy_id),
                        str(vacancy_name),
                        0,
                        int(vacancy_sal_to),
                        str(vacancy_url),
                        int(vacancy_employer_id)
                    ),
                )
    conn.commit()
    conn.close()
    return "База данных заполнена"


class DBManager:
    """Класс для работы в базе данных с вакансиями и компаниями"""

    def __init__(self):
        load_dotenv()
        self.conn = psycopg2.connect(
            db_name=os.getenv("dbname"),
            host=os.getenv("host"),
            user=os.getenv("user"),
            database="api_db",
            password=os.getenv("password"),
        )

    def get_companies_and_vacancies_count(self) -> list:
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT name, open_vacancies FROM company
                """
            )
            result = cur.fetchall()
            conn.commit()
            conn.close()
        return result

    def get_all_vacancies(self) -> Any:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        load_dotenv()
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM vacancies
                """
            )
            total = cur.fetchall()
            conn.commit()
            conn.close()
        return total

    def get_avg_salary(self) -> list:
        """
        Получает среднюю зарплату по вакансиям
        """
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                """
                 SELECT ((SUM(salary_to) + SUM(salary_from)) / 2) / COUNT(*) AS avg_salary FROM vacancies
                """
            )
            avg_salary = cur.fetchone()[0]
            conn.commit()
        return avg_salary

    def get_vacancies_with_higher_salary(self) -> list:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """
        conn = self.conn
        avg_salary = self.get_avg_salary()
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM vacancies WHERE (salary_to + salary_from) / 2 > %s
                """,
                [avg_salary],
            )
            vacancies = cur.fetchall()
            conn.commit()
            conn.close()
        return vacancies

    def get_vacancies_with_keyword(self, word: str) -> list:
        """
        Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python
        """
        conn = self.conn
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM vacancies WHERE name ILIKE %s
                """,
                ("%" + word + "%",),
            )
            result = cur.fetchall()
            conn.commit()
        conn.close()
        return result
