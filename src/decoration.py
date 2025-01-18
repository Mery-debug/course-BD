from typing import Any, Callable
from functools import wraps
from beautifultable import BeautifulTable


def wrapper(func: Callable) -> Callable:
    """Декоратор для выведения результатов в таблицу"""

    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> Any:
        comp = func(*args, **kwargs)
        table = BeautifulTable()
        table.column_headers = comp[0].keys()
        for dic in comp:
            table.append_row(list(dic.values()))

        return table

    return inner

