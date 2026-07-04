import asyncio
import signal
from types import FrameType

import globalvars
import connection.welcomer as welcomer


async def main():
    signal.signal(signal.SIGTERM, exit_gracefully)
    signal.signal(signal.SIGINT, exit_gracefully)

    asyncio.gather(welcomer.broadcast_listener())

    while not globalvars.kill_now:
        # print("xablau")
        pass


def exit_gracefully(signum: int, frame: FrameType | None):
    print(f"singal {signal.Signals(signum).name} received, closing...")
    globalvars.kill_now = True


if __name__ == "__main__":
    asyncio.run(main())
