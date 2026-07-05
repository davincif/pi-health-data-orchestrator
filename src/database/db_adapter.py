from abc import ABC, abstractmethod
from typing import Any

from models.data_types import IncomingMutableUpdate, IncomingUnmutableUpdate


class DBAdapter(ABC):

    @abstractmethod
    def connect(self, conf: Any):
        return self

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def register_device(self, data: Any):
        pass

    @abstractmethod
    def update_health_check(self, health: IncomingMutableUpdate):
        pass

    @abstractmethod
    def update_device(self, device_info: IncomingUnmutableUpdate):
        pass
