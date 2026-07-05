from __future__ import annotations

import enum
import json
import os
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Engine,
    Enum,
    Float,
    ForeignKey,
    String,
    Integer,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)


class HardwareType(enum.Enum):
    CPU = "cpu"
    GPU = "gpu"


class Base(DeclarativeBase):
    pass


class EnLabel(Base):
    __tablename__ = "en_labels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    translation: Mapped[str] = mapped_column(String, nullable=False)


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    core: Mapped[int | None] = mapped_column(Integer, nullable=True)
    logical_core: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_freq: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_freq: Mapped[float | None] = mapped_column(Float, nullable=True)
    virtual_memory_total: Mapped[int | None] = mapped_column(Integer, nullable=True)
    swap_memory_total: Mapped[int | None] = mapped_column(Integer, nullable=True)
    boot_time: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_collection_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    cores: Mapped[list[DeviceCore]] = relationship(back_populates="device")
    temperatures: Mapped[list[Temperature]] = relationship(back_populates="device")
    processes: Mapped[list[Process]] = relationship(back_populates="device")
    virtual_memories: Mapped[list[VirtualMemory]] = relationship(
        back_populates="device"
    )
    swap_memories: Mapped[list[SwapMemory]] = relationship(back_populates="device")
    disks: Mapped[list[Disk]] = relationship(back_populates="device")
    watcher_disks: Mapped[list[WatcherDisk]] = relationship(back_populates="device")
    networks: Mapped[list[Network]] = relationship(back_populates="device")
    update_costs: Mapped[list[UpdateCost]] = relationship(back_populates="device")


class DeviceCore(Base):
    __tablename__ = "device_cores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)
    index: Mapped[int] = mapped_column(Integer, nullable=False)
    min_freq: Mapped[float] = mapped_column(Float, nullable=False)
    max_freq: Mapped[float] = mapped_column(Float, nullable=False)

    device: Mapped[Device] = relationship(back_populates="cores")


class Temperature(Base):
    __tablename__ = "temperatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)
    hardware: Mapped[HardwareType] = mapped_column(Enum(HardwareType), nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)
    current: Mapped[float] = mapped_column(Float, nullable=True)
    high: Mapped[float] = mapped_column(Float, nullable=True)
    critical: Mapped[float] = mapped_column(Float, nullable=True)
    registred_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    device: Mapped[Device] = relationship(back_populates="temperatures")


class Process(Base):
    __tablename__ = "process"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)
    load: Mapped[float | None] = mapped_column(Float, nullable=True)
    index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    one_minute_avarage: Mapped[float | None] = mapped_column(
        "1_minute_avarage", Float, nullable=True
    )
    five_minute_avarage: Mapped[float | None] = mapped_column(
        "5_minute_avarage", Float, nullable=True
    )
    fifteen_minute_avarage: Mapped[float | None] = mapped_column(
        "15_minute_avarage", Float, nullable=True
    )
    user: Mapped[float | None] = mapped_column(Float, nullable=True)
    system: Mapped[float | None] = mapped_column(Float, nullable=True)
    idle: Mapped[float | None] = mapped_column(Float, nullable=True)
    nice: Mapped[float | None] = mapped_column(Float, nullable=True)
    iowait: Mapped[float | None] = mapped_column(Float, nullable=True)
    user_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    system_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    idle_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    nice_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    iowait_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    current_frequency: Mapped[float | None] = mapped_column(Float, nullable=True)
    registred_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    device: Mapped[Device] = relationship(back_populates="processes")


class VirtualMemory(Base):
    __tablename__ = "virtual_memories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    used: Mapped[int | None] = mapped_column(Integer)
    free: Mapped[int | None] = mapped_column(Integer)
    percent: Mapped[float | None] = mapped_column(Float)
    available: Mapped[int] = mapped_column(Integer, nullable=False)
    active: Mapped[int] = mapped_column(Integer, nullable=False)
    inactive: Mapped[int] = mapped_column(Integer, nullable=False)
    buffers: Mapped[int] = mapped_column(Integer, nullable=False)
    cached: Mapped[int] = mapped_column(Integer, nullable=False)
    shared: Mapped[int] = mapped_column(Integer, nullable=False)
    slab: Mapped[int] = mapped_column(Integer, nullable=False)
    registred_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    device: Mapped[Device | None] = relationship(back_populates="virtual_memories")


class SwapMemory(Base):
    __tablename__ = "swap_memories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    used: Mapped[int | None] = mapped_column(Integer)
    free: Mapped[int | None] = mapped_column(Integer)
    percent: Mapped[float | None] = mapped_column(Float)
    sin: Mapped[int | None] = mapped_column(Integer)
    sout: Mapped[int | None] = mapped_column(Integer)
    registred_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    device: Mapped[Device | None] = relationship(back_populates="swap_memories")


class Disk(Base):
    __tablename__ = "disks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    total: Mapped[int | None] = mapped_column(Integer)
    used: Mapped[int | None] = mapped_column(Integer)
    free: Mapped[int | None] = mapped_column(Integer)
    percent: Mapped[float | None] = mapped_column(Float)
    registred_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    device: Mapped[Device | None] = relationship(back_populates="disks")


class WatcherDisk(Base):
    __tablename__ = "watcher_disks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    read_count: Mapped[int | None] = mapped_column(Integer)
    write_count: Mapped[int | None] = mapped_column(Integer)
    read_bytes: Mapped[int | None] = mapped_column(Integer)
    write_bytes: Mapped[int | None] = mapped_column(Integer)
    read_time: Mapped[int | None] = mapped_column(Integer)
    write_time: Mapped[int | None] = mapped_column(Integer)
    busy_time: Mapped[int | None] = mapped_column(Integer)
    registred_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    device: Mapped[Device | None] = relationship(back_populates="watcher_disks")


class Network(Base):
    __tablename__ = "networks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    bytes_sent: Mapped[int] = mapped_column(Integer, nullable=False)
    bytes_recv: Mapped[int] = mapped_column(Integer, nullable=False)
    packets_sent: Mapped[int] = mapped_column(Integer, nullable=False)
    packets_recv: Mapped[int] = mapped_column(Integer, nullable=False)
    errin: Mapped[int] = mapped_column(Integer, nullable=False)
    errout: Mapped[int] = mapped_column(Integer, nullable=False)
    dropin: Mapped[int] = mapped_column(Integer, nullable=False)
    dropout: Mapped[int] = mapped_column(Integer, nullable=False)
    registred_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    device: Mapped[Device | None] = relationship(back_populates="networks")


class UpdateCost(Base):
    __tablename__ = "update_costs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("devices.id"))
    lst_cost: Mapped[float] = mapped_column(Float, nullable=False)
    registred_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    device: Mapped[Device | None] = relationship(back_populates="update_costs")


def make_db(engine: Engine):
    Base.metadata.create_all(engine, checkfirst=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    __populate_translations(session)
    session.commit()


def __populate_translations(session: Session):
    translations: dict[str, str]
    json_path = os.path.join(os.path.dirname(__file__), "en_symbol_translation.json")
    with open(json_path, "r") as en_file:
        translations = json.load(en_file)

    for key in translations.keys():
        newTranslation = EnLabel(symbol=key, translation=translations[key])
        session.add(newTranslation)
