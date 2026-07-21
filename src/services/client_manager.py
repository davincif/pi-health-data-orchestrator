from typing import Any

from database import db_factory


from database.db_adapter import DBAdapter
from models.data_types import (
    IncomingMutableUpdate,
    IncomingUnmutableUpdate,
)


class ClientManager:
    db: DBAdapter

    def __init__(self, conf: Any) -> None:
        print("ClientManager")
        self.db = db_factory.new_db().connect(conf)
        print("self.db", self.db)

    def close(self):
        self.db.close()

    def update_health_check(self, data: IncomingUnmutableUpdate):
        self.db.update_health_check(data)

    def update_unmutable(self, data: IncomingMutableUpdate):
        self.db.update_device(data)

    # def __get_client_key(self, data: InOutMsgBase) -> str:
    #     return data["requester"] if "requester" in data else ""
