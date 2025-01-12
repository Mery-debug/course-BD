from src.API import APIhh


def user_params():
    """Функция для взаимодействия с пользователем"""
    print('Введите слово для поиска по работодателям')
    search = input()
    employers = APIhh.search_api_hh_clients(search)
    if not employers:
        print('По вашему запросу ничего не найдено')
        return
    return search

