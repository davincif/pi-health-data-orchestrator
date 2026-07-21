from datetime import datetime, timedelta
import os
import sqlite3
import threading
from time import perf_counter, sleep
from typing import Any, cast

from sqlalchemy import (
    Connection,
    Engine,
    StaticPool,
    create_engine,
    select,
)
from sqlalchemy.orm import Session, sessionmaker

import globalvars
from utils.dict_utils import get_item_else

from .models.data_description import (
    Device,
    Disk,
    HardwareType,
    Temperature,
    Process,
    UpdateCost,
    VirtualMemory,
    SwapMemory,
    Disk,
    Network,
    WatcherDisk,
    make_db,
)
from models.data_types import (
    IncomingMutableUpdate,
    IncomingUnmutableUpdate,
)

from .db_adapter import DBAdapter


class SQLiteImpl(DBAdapter):
    memory_db: Engine
    memory_db_conn: Connection
    _shared_memory_conn: sqlite3.Connection

    backup_counter: float = 0.0
    backup_mark: float = 0.0

    _renewal_lock = threading.Lock()

    def connect(self, conf: Any):
        self._shared_memory_conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.memory_db = create_engine(
            "sqlite://",
            creator=lambda: self._shared_memory_conn,
            poolclass=StaticPool,
        )
        self.memory_db_conn = self.memory_db.connect()

        self.file_addrs = self.__make_file_name(conf)
        self.__reload_db()

        self.backup_counter = 0.0
        self.backup_mark = perf_counter()

        threading.Thread(target=self.__set_db_periodic_renewal, args=[conf]).start()

        return self

    def close(self):
        with self._renewal_lock:
            self.__backup()
            self.memory_db_conn.close()
            self.memory_db.dispose()
            if hasattr(self, "_shared_memory_conn") and self._shared_memory_conn:
                self._shared_memory_conn.close()

    def update_health_check(self, health: IncomingMutableUpdate):
        print("\nupdate_health_check", health, "\n")
        with self._renewal_lock:
            session = self.__get_new_section()

            user = (
                session.query(Device).filter(Device.name == health["requester"]).first()
            )
            if user is None:
                return

            time: float | None = get_item_else(health, 0.0, "now")
            now = datetime.fromtimestamp(time) if time != 0.0 else None
            user.last_collection_at = now

            cpu, gpu = self.__add_temperature(user.id, now, health)
            session.add(cpu)
            session.add(gpu)

            [process, cores] = self.__add_process(user.id, now, health)
            session.add(process)
            for core in cores:
                session.add(core)

            [vmem, smem] = self.__add_memory(user.id, now, health)
            session.add(vmem)
            session.add(smem)

            disk = self.__add_disk(user.id, now, health)
            session.add(disk)

            net = self.__add_network(user.id, now, health)
            session.add(net)

            cost = self.__add_cost(user.id, now, health)
            session.add(cost)

            session.commit()
            session.close()

            self.__update_backup()

    def update_device(self, device_info: IncomingUnmutableUpdate):
        print("update_device")
        with self._renewal_lock:
            print("device_info", device_info)
            session = self.__get_new_section()

            user = (
                session.query(Device)
                .filter(Device.name == device_info["requester"])
                .first()
            )
            if user is None:
                user = self.__register_device(
                    session,
                    device_info,
                )
            print("user", user)
            if user is None:
                return

            try:
                time: float | None = get_item_else(device_info, 0.0, "now")
                now = datetime.fromtimestamp(time) if time != 0.0 else None

                user.last_collection_at = now
                user.boot_time = get_item_else(device_info, 0, "uptime", "bt")
                user.core = get_item_else(device_info, 0, "process", "cr")
                user.logical_core = get_item_else(device_info, 0, "process", "lcr")
                user.min_freq = get_item_else(device_info, 0, "process", "mnf")
                user.max_freq = get_item_else(device_info, 0, "process", "mxf")
                user.virtual_memory_total = get_item_else(
                    device_info, 0, "memory", "v", "t"
                )
                user.swap_memory_total = get_item_else(
                    device_info, 0, "memory", "s", "t"
                )

                disk = session.query(Disk).filter(Disk.device_id == user.id).first()
                if disk is None:
                    disk = Disk(device_id=user.id, registred_at=now)
                else:
                    disk.registred_at = now  # type: ignore

                disk.total = get_item_else(device_info, 0, "disk", "t")
                disk.used = get_item_else(device_info, 0, "disk", "u")
                disk.free = get_item_else(device_info, 0, "disk", "f")
                disk.percent = get_item_else(device_info, 0.0, "disk", "p")

                session.add(disk)
                session.commit()
            except Exception as exp:
                print("exp", exp)

            session.close()

    def __get_new_section(self):
        Session = sessionmaker(bind=self.memory_db)
        return Session()

    def __backup(self):
        print("__backup")
        source_raw = cast(
            sqlite3.Connection, self.memory_db_conn.connection.dbapi_connection
        )

        target_raw = None
        try:
            target_raw = sqlite3.connect(self.file_addrs, check_same_thread=False)
            source_raw.backup(target_raw)
            print("backup done!")
        except Exception as exp:
            print("deu bósnia no backup!", exp)
            pass
        finally:
            if target_raw:
                target_raw.close()

    def __make_file_name(self, conf: Any) -> str:
        now = datetime.now()

        return os.path.join(
            globalvars.DB_PATH,
            (
                "{:02d}".format(now.day)
                + "-"
                + "{:02d}".format(now.month)
                + "-"
                + str(now.year)
                + "."
                + conf["db_addrs"]
            ),
        )

    def __reload_db(self):
        does_db_exists = (
            os.path.exists(self.file_addrs) and os.path.getsize(self.file_addrs) > 0
        )

        if does_db_exists:
            hard_db_conn = sqlite3.connect(self.file_addrs)
            source_raw = cast(
                sqlite3.Connection, self.memory_db_conn.connection.dbapi_connection
            )
            try:
                hard_db_conn.backup(source_raw)
            finally:
                hard_db_conn.close()
        else:
            make_db(self.memory_db)

    def __add_temperature(
        self, device_id: int, now: datetime | None, health: IncomingMutableUpdate
    ) -> tuple[Temperature, Temperature]:

        temp_cpu = Temperature(
            device_id=device_id,
            hardware=HardwareType.CPU,
            label=get_item_else(health, "", "temp", "cpu", "lb"),
            current=get_item_else(health, None, "temp", "cpu", "curr"),
            high=get_item_else(health, None, "temp", "cpu", "high"),
            critical=get_item_else(health, None, "temp", "cpu", "crit"),
            registred_at=now,
        )

        temp_gpu = Temperature(
            device_id=device_id,
            hardware=HardwareType.GPU,
            label=get_item_else(health, "", "temp", "gpu", "lb"),
            current=get_item_else(health, 0.0, "temp", "gpu", "curr"),
            high=get_item_else(health, 0.0, "temp", "gpu", "high"),
            critical=get_item_else(health, 0.0, "temp", "gpu", "crit"),
            registred_at=now,
        )

        return (temp_cpu, temp_gpu)

    def __add_process(
        self, device_id: int, now: datetime | None, health: IncomingMutableUpdate
    ) -> tuple[Process, list[Process]]:
        p_data = get_item_else(health, {}, "process")

        process = Process(
            device_id=device_id,
            index=0,
            load=get_item_else(p_data, 0.0, "load"),
            one_minute_avarage=get_item_else(p_data, 0.0, "1min"),
            five_minute_avarage=get_item_else(p_data, 0.0, "5min"),
            fifteen_minute_avarage=get_item_else(p_data, 0.0, "15min"),
            user=get_item_else(p_data, 0.0, "user"),
            system=get_item_else(p_data, 0.0, "sys"),
            idle=get_item_else(p_data, 0.0, "idle"),
            nice=get_item_else(p_data, 0.0, "nice"),
            iowait=get_item_else(p_data, 0.0, "io"),
            user_percent=get_item_else(p_data, 0.0, "userp"),
            system_percent=get_item_else(p_data, 0.0, "sysp"),
            idle_percent=get_item_else(p_data, 0.0, "idlep"),
            nice_percent=get_item_else(p_data, 0.0, "nicep"),
            iowait_percent=get_item_else(p_data, 0.0, "iop"),
            current_frequency=get_item_else(p_data, 0.0, "cfreq"),
            registred_at=now,
        )

        logi_cores: list[Process] = []
        lcrinfo = get_item_else(health, [], "process", "lcrinfo")

        for index, core in enumerate(lcrinfo):
            logi_cores.append(
                Process(
                    device_id=device_id,
                    index=index + 1,
                    load=get_item_else(core, 0.0, "load"),
                    one_minute_avarage=get_item_else(core, 0.0, "1min"),
                    five_minute_avarage=get_item_else(core, 0.0, "5min"),
                    fifteen_minute_avarage=get_item_else(core, 0.0, "15min"),
                    user=get_item_else(core, 0.0, "user"),
                    system=get_item_else(core, 0.0, "sys"),
                    idle=get_item_else(core, 0.0, "idle"),
                    nice=get_item_else(core, 0.0, "nice"),
                    iowait=get_item_else(core, 0.0, "io"),
                    user_percent=get_item_else(core, 0.0, "userp"),
                    system_percent=get_item_else(core, 0.0, "sysp"),
                    idle_percent=get_item_else(core, 0.0, "idlep"),
                    nice_percent=get_item_else(core, 0.0, "nicep"),
                    iowait_percent=get_item_else(core, 0.0, "iop"),
                    current_frequency=get_item_else(core, 0.0, "cfreq"),
                    registred_at=now,
                )
            )

        return (process, logi_cores)

    def __add_memory(
        self, device_id: int, now: datetime | None, health: IncomingMutableUpdate
    ) -> tuple[VirtualMemory, SwapMemory]:
        vmemory = get_item_else(health, 0, "memory", "v")
        vmem = VirtualMemory(
            device_id=device_id,
            used=get_item_else(vmemory, 0, "avlb"),
            free=get_item_else(vmemory, 0, "p"),
            percent=get_item_else(vmemory, 0.0, "u"),
            available=get_item_else(vmemory, 0, "f"),
            active=get_item_else(vmemory, 0, "ac"),
            inactive=get_item_else(vmemory, 0, "in"),
            buffers=get_item_else(vmemory, 0, "bff"),
            cached=get_item_else(vmemory, 0, "ca"),
            shared=get_item_else(vmemory, 0, "sh"),
            slab=get_item_else(vmemory, 0, "sl"),
            registred_at=now,
        )

        smemory = get_item_else(health, 0, "memory", "s")
        smem = SwapMemory(
            device_id=device_id,
            used=get_item_else(smemory, 0, "u"),
            free=get_item_else(smemory, 0, "f"),
            percent=get_item_else(smemory, 0.0, "p"),
            sin=get_item_else(smemory, 0, "si"),
            sout=get_item_else(smemory, 0, "so"),
            registred_at=now,
        )

        return (vmem, smem)

    def __add_disk(
        self, device_id: int, now: datetime | None, health: IncomingMutableUpdate
    ) -> WatcherDisk:
        disk = WatcherDisk(
            device_id=device_id,
            read_count=get_item_else(health, 0, "rc"),
            registred_at=now,
        )

        return disk

    def __add_network(
        self, device_id: int, now: datetime | None, health: IncomingMutableUpdate
    ) -> Network:
        net = Network(
            device_id=device_id,
            bytes_sent=get_item_else(health, 0, "bs"),
            bytes_recv=get_item_else(health, 0, "br"),
            packets_sent=get_item_else(health, 0, "ps"),
            packets_recv=get_item_else(health, 0, "pr"),
            errin=get_item_else(health, 0, "ei"),
            errout=get_item_else(health, 0, "eo"),
            dropin=get_item_else(health, 0, "di"),
            dropout=get_item_else(health, 0, "do"),
            registred_at=now,
        )

        return net

    def __add_cost(
        self, device_id: int, now: datetime | None, health: IncomingMutableUpdate
    ) -> UpdateCost:
        cost = UpdateCost(
            device_id=device_id,
            lst_cost=get_item_else(health, -1, "lct"),
            registred_at=now,
        )

        return cost

    def __update_backup(self):
        self.backup_counter = perf_counter()

        if self.backup_counter - self.backup_mark > globalvars.db_back_rate_s:
            self.__backup()

    def __set_db_periodic_renewal(self, conf: Any):
        while True:
            target_hour = 0
            target_minute = 0

            now = datetime.now()
            target_time = now.replace(
                hour=target_hour, minute=target_minute, second=0, microsecond=0
            )

            if now > target_time:
                target_time += timedelta(days=1)

            seconds_to_wait = (target_time - now).total_seconds()
            print(f"Sleeping for {seconds_to_wait} seconds until {target_time}...")

            # TODO REMOVE THIS TEST!
            seconds_to_wait = 60
            sleep(seconds_to_wait)
            self.__renewal(conf)

    def __renewal(self, conf: Any):
        print("__renewal")
        self.close()

        with self._renewal_lock:

            self._shared_memory_conn = sqlite3.connect(
                ":memory:", check_same_thread=False
            )
            self.memory_db = create_engine(
                "sqlite://",
                creator=lambda: self._shared_memory_conn,
                poolclass=StaticPool,
            )
            self.memory_db_conn = self.memory_db.connect()

            self.file_addrs = self.__make_file_name(conf)

            self.__reload_db()

            self.backup_counter = 0.0
            self.backup_mark = perf_counter()

    def __register_device(self, session: Session, data: IncomingUnmutableUpdate):
        with self._renewal_lock:

            stmt = select(Device).where(Device.name == data["requester"])
            found_device = session.scalar(stmt)

            if found_device:
                return

            device = Device(
                name=data["requester"],
            )

            session.add(device)

            return device
