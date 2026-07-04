import asyncio
import socket

import globalvars
import connection.authentication as authentication

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


async def broadcast_listener():
    """watching for new connections"""
    print("watching for new connections")

    sock.setblocking(False)
    sock.bind((globalvars.AUTO_CONNECT_ADDRESS, globalvars.AUTO_CONNECT_PORT))
    loop = asyncio.get_running_loop()

    print("Socket bound, waiting for newcomers...")
    try:
        while not globalvars.kill_now:
            data, addr = await loop.sock_recvfrom(sock, 512)
            asyncio.create_task(new_commer_handler(data, addr))
    except asyncio.CancelledError:
        print("Broadcast listener cancelled.")
    finally:
        print("Closing welcomer socket.")
        sock.close()


async def new_commer_handler(data: bytes, addr: str):
    auth = authentication.authenticate(data)
    if not auth:
        return

    loop = asyncio.get_running_loop()
    await loop.sock_sendto(sock, auth.encode(), addr)
