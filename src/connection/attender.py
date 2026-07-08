import json
import threading
from time import sleep
import websockets.sync.server
import websockets.exceptions

import globalvars
from models.data_types import InOutMsgBase


def attend():
    print(
        f"WebSocket Server started @ {globalvars.SERVER_ADDRESS}:{globalvars.SERVER_PORT}"
    )

    server = websockets.sync.server.serve(
        __data_handler, globalvars.SERVER_ADDRESS, globalvars.SERVER_PORT
    )

    # globalvars.read_for_new_connetion_lock.release()
    print("WebSocket online.")

    threading.Thread(target=__watch_kill, args=[server], daemon=True).start()

    server.serve_forever()
    print("WebSocket Server closed.")


# watcher thread to shut the server down when kill_now is set
def __watch_kill(server: websockets.sync.server.Server):
    while not globalvars.kill_now:
        sleep(2)
    server.shutdown()


def __data_handler(websocket: websockets.sync.server.ServerConnection):
    try:
        for message in websocket:
            if globalvars.kill_now:
                break
            # print(f"Recebido de {websocket.remote_address}: {message}")
            data: InOutMsgBase = json.loads(message)

            if not "command" in data:
                continue
            if data["command"] == "helth-check-info":
                globalvars.client_manager.update_health_check(data)
            elif data["command"] == "update-unmutable":
                globalvars.client_manager.update_unmutable(data)
    except websockets.exceptions.ConnectionClosedError:
        print(f"Cliente {websocket.remote_address} desconectado.")
