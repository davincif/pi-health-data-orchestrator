from typing import Any


def get_item_else[T](
    _dict: Any,
    default: T,
    *args,
) -> T:
    value = default
    dict_pointer = _dict

    for arg in args:
        if arg in dict_pointer:
            value = dict_pointer[arg]
            if isinstance(value, dict):
                dict_pointer = value
        else:
            return default

    return value


# def __get_from[T](session: Session, SearchClass: T, **kwargs) -> T | None:
#     for kwarg in kwargs:
#         found = (
#             session.query(SearchClass)
#             .filter(SearchClass["kwarg"] == kwargs[kwarg])
#             .first()
#         )
#         if found is not None:
#             return found

#     return None
