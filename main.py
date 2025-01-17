from src.API import APIhh
from src.DBManager import create_database, save_data_to_database, DBManager
from src.decoration import wrapper
from src.user_utils import user_params


@wrapper
def main():
    u = user_params()
    a = list(APIhh(u).search_api_hh_clients())
    print(a)
    v = list(APIhh(u).search_api_vacancies(a))
    print(v)
    create_database()
    save_data_to_database(a, v)
    user_1 = int(input('какое действие с базой данных хотите произвести?'
                   '1. Получить список всех компаний и количество вакансий у каждой компании.'
                   '2. Получить список всех вакансий.'
                   '3. Получить среднюю зарплату по вакансиям.'
                   '4. Получить список вакансий с зарплатой выше средней.'
                   '5. Получить список всех вакансий, в названии которых есть искомое слово.'))
    if user_1 == 1:
        result = DBManager().get_companies_and_vacancies_count()
    elif user_1 == 2:
        result = DBManager().get_all_vacancies()
    elif user_1 == 3:
        result = DBManager().get_avg_salary()
    elif user_1 == 4:
        result = DBManager().get_vacancies_with_higher_salary()
    elif user_1 == 5:
        result = DBManager().get_vacancies_with_keyword(u)
    else:
        return [{"Ничего не найдено": "Ничего не найдено"}]
    return result


if __name__ == "__main__":
    p = main()
    print(p)
