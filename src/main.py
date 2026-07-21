import threading
import signal
from types import FrameType

from controllers import attender
import globalvars


def main():
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    print(
        f"raspbarry-health-data-collector version: {globalvars.version}\nby - davincif\ncheck me @ ldavincif.com\n"
    )

    threading.Thread(target=attender.attend).start()


def exit_gracefully(signum: int, frame: FrameType | None):
    print(f"signal {signal.Signals(signum).name} received, closing...")

    globalvars.kill_now = True
    globalvars.client_manager.close()


if __name__ == "__main__":
    main()
