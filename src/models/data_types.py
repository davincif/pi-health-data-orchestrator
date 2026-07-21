from multiprocessing import Process
from typing import Literal, TypedDict, Required

from .update_mutable import MDisk, MNet, MProcess, MTemp, MMemory

from .update_unmutable import UMDisk, UMMemory, UMUptime

type Addr = tuple[str, int]


class InOutMsgBase(TypedDict):
    requester: Required[str]
    command: Required[
        Literal["connect", "disconnect", "update-unmutable", "helth-check-info"]
    ]


class IncomingClientRegistry(InOutMsgBase):
    addr: Required[Addr]


class TransitionalClientRegistry(InOutMsgBase):
    requester: Required[str]
    addr: str
    port: int


class IncomingUnmutableUpdate(InOutMsgBase, total=False):
    uptime: UMUptime
    process: Process
    memory: UMMemory
    disk: UMDisk
    now: float


class IncomingMutableUpdate(InOutMsgBase, total=False):
    temp: MTemp
    process: MProcess
    memory: MMemory
    disk: MDisk
    net: MNet
    now: float
    lct: int
