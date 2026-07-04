import asyncio
import signal
from types import FrameType

from connection import welcomer
from connection import attender
import globalvars

welcome: asyncio.Task[None]
attending: asyncio.Task[None]


async def main():
    global welcome, attending

    signal.signal(signal.SIGTERM, exit_gracefully)
    signal.signal(signal.SIGINT, exit_gracefully)

    welcome = asyncio.create_task(welcomer.broadcast_listener())
    attending = asyncio.create_task(attender.attend())

    await asyncio.gather(welcome, attending)


def exit_gracefully(signum: int, frame: FrameType | None):
    global welcome, attending

    print(f"signal {signal.Signals(signum).name} received, closing...")

    globalvars.kill_now = True
    print("welcome", welcome.cancel(), "\n")
    print("attending", attending.cancel(), "\n")


if __name__ == "__main__":
    asyncio.run(main())
