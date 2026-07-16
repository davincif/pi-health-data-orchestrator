from typing import Any

from database import db_factory

from .db_adapter import DBAdapter

from models.data_types import (
    InOutMsgBase,
    IncomingClientRegistry,
    IncomingMutableUpdate,
    IncomingUnmutableUpdate,
    TransitionalClientRegistry,
)


class ClientManager:
    clients_map: dict[str, TransitionalClientRegistry] = {}
    db: DBAdapter

    def __init__(self, conf: Any) -> None:
        self.db = db_factory.new_db().connect(conf)

    # def add(self, newClient: IncomingClientRegistry) -> bool:
    #     key = self.__get_client_key(newClient)
    #     if self.clients_map.get(key) is not None:
    #         return False

    #     client: TransitionalClientRegistry = {
    #         **newClient,
    #         "addr": newClient["addr"][0],
    #         "port": newClient["addr"][1],
    #     }

    #     self.clients_map[key] = client
    #     self.db.register_device(client)

    #     return True

    def remove(self, client4Removal: IncomingClientRegistry) -> bool:
        if self.clients_map.get(client4Removal["requester"]) is None:
            return False

        self.clients_map.pop(client4Removal["requester"])
        return True

    def close(self):
        self.db.close()

    def update_health_check(self, data: IncomingUnmutableUpdate):
        key = self.__get_client_key(data)
        if self.clients_map.get(key) is None:
            return

        self.db.update_health_check(data)

    def update_unmutable(self, data: IncomingMutableUpdate):
        key = self.__get_client_key(data)
        if self.clients_map.get(key) is None:
            return

        self.db.update_device(data)

    def __get_client_key(self, data: InOutMsgBase) -> str:
        return data["requester"] if "requester" in data else ""
