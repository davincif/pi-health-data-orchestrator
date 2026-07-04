from time import time
import json
import socket
import threading

import globalvars

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def broadcast_listener():
    """watching for new connections"""
    print("watching for new connections")

    # sock.setblocking(False)
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


def newcomer_handler(data: bytes, addr: str):
    print("newcomer!")
    print("msg", data)
    print("addr", addr)

    resp = {
        "port": globalvars.SERVER_PORT,
        "now": time(),
        # "addr": sock.getsockname()[0],
        # "version": globalvars.version,
    }

    sock.sendto(json.dumps(resp).encode(), addr)
