from typing import List, TypedDict


class UMDisk(TypedDict):
    t: int
    u: int
    f: int
    p: float


class UMMemoryInfo(TypedDict):
    t: int


class UMMemory(TypedDict):
    v: UMMemoryInfo
    s: UMMemoryInfo


class UMLcrinfo(TypedDict):
    mnf: int
    mxf: int


class UMProcess(TypedDict):
    cr: int
    lcr: int
    mnf: int
    mxf: int
    lcrinfo: List[UMLcrinfo]


class UMUptime(TypedDict):
    bt: int
