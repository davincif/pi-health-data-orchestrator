from typing import List, Dict, TypedDict


class MDisk(TypedDict):
    rc: int
    wc: int
    rb: int
    wb: int
    rt: int
    wt: int
    bt: int


class MSwapMem(TypedDict):
    u: int
    f: int
    p: int
    si: int
    so: int


class MVirtualMem(TypedDict):
    avlb: int
    p: float
    u: int
    f: int
    ac: int
    v_in: int
    bff: int
    ca: int
    sh: int
    sl: int


class MMemory(TypedDict):
    v: MVirtualMem
    s: MSwapMem


class MNet(TypedDict):
    bs: int
    br: int
    ps: int
    pr: int
    ei: int
    eo: int
    di: int
    do: int


class MProcess(TypedDict):
    load: float
    the_1_min: float
    the_5_min: float
    the_15_min: float
    user: float
    sys: float
    idle: float
    nice: float
    io: float
    userp: float
    sysp: float
    idlep: float
    nicep: int
    iop: float
    cfreq: float
    lcrinfo: List[Dict[str, float]]


class MCPU(TypedDict):
    lb: str
    curr: int
    high: None
    crit: None


class MTemp(TypedDict):
    cpu: MCPU
    gpu: MCPU
