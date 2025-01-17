from src.API import APIhh


def user_params():
    """Функция для взаимодействия с пользователем"""
    print('Введите слово для поиска по работодателям')
    search = input()
    employers = APIhh(search).search_api_hh_clients()
    if not employers:
        print('По вашему запросу ничего не найдено')
        return
    return search

