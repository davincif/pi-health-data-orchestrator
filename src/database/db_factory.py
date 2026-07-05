from .sqlite_impl import SQLiteImpl

from .db_adapter import DBAdapter


def new_db() -> DBAdapter:
    return SQLiteImpl()
