import threading
import signal
from types import FrameType

from connection import attender
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

    attending = threading.Thread(target=attender.attend)
    # globalvars.read_for_new_connetion_lock.acquire()
    attending.start()

    # welcome = threading.Thread(target=welcomer.broadcast_listener)
    # globalvars.read_for_new_connetion_lock.acquire()
    # welcome.start()


def exit_gracefully(signum: int, frame: FrameType | None):
    print(f"signal {signal.Signals(signum).name} received, closing...")

    globalvars.kill_now = True
    globalvars.client_manager.close()


if __name__ == "__main__":
    main()
