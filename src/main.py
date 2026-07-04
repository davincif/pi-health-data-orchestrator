import threading
import signal
from types import FrameType
from connection import welcomer, attender

import globalvars

welcome: threading.Thread
attending: threading.Thread


def main():
    global welcome, attending

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    print(
        f"raspbarry-health-data-collector version: {globalvars.version}\nby - davincif\ncheck me @ ldavincif.com\n"
    )

    globalvars.read_for_new_connetion_lock.acquire()
    attending = threading.Thread(target=attender.attend)
    attending.start()

    welcome = threading.Thread(target=welcomer.broadcast_listener)
    globalvars.read_for_new_connetion_lock.acquire()
    welcome.start()


def exit_gracefully(signum: int, frame: FrameType | None):
    global welcome, attending

    print(f"signal {signal.Signals(signum).name} received, closing...")

    globalvars.kill_now = True


if __name__ == "__main__":
    main()
