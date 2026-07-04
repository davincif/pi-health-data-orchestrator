import asyncio
import socket

import globalvars
import connection.authentication as authentication

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


async def broadcast_listener():
    """watching for new connections"""
    print("watching for new connections")

    global kill_now, sock

    sock.bind(("", globalvars.AUTO_CONNECT_PORT))

    print("sock", sock)
    while not globalvars.kill_now:
        print("waiting for newcommeres")
        data, addr = sock.recvfrom(512)
        asyncio.run(new_msg_handler(data, addr))


async def new_msg_handler(data: bytes, addr: str):
    auth = authentication.authenticate(data)
    if not auth:
        return

    sock.sendto(auth.encode(), addr)
