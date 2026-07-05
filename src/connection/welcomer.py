from time import time
import json
import socket
import threading


import globalvars
from models.data_types import IncomingClientRegistry

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def broadcast_listener():
    """watching for new connections"""
    print("watching for new connections")

    sock.settimeout(globalvars.update_rate * 2.0)
    sock.bind((globalvars.AUTO_CONNECT_ADDRESS, globalvars.AUTO_CONNECT_PORT))
    print("Socket bound, waiting for newcomers...")

    while not globalvars.kill_now:
        try:
            data, addr = sock.recvfrom(512)
        except socket.timeout:
            continue

        if data:
            attending = threading.Thread(target=newcomer_handler, args=(data, addr))
            attending.start()


def newcomer_handler(data: bytes, addr: tuple[str, int]):
    print("newcomer!")
    print("msg", data)
    print("addr", addr)

    registry = IncomingClientRegistry(json.loads(data.decode()))
    registry["addr"] = addr

    if registry["command"] != "connect":
        return

    was_registred = globalvars.client_manager.add(registry)

    if was_registred:
        resp = {
            "port": globalvars.SERVER_PORT,
            "now": time(),
            # "addr": sock.getsockname()[0],
            "version": globalvars.version,
        }
    else:
        resp = {
            "error": {"msg": "client already registrated"},
            "version": globalvars.version,
        }

    sock.sendto(json.dumps(resp).encode(), addr)
