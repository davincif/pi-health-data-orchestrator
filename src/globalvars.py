import threading

kill_now = False
version = "0.0.1"
verbose = False

update_rate = 0.9
read_for_new_connetion_lock = threading.Lock()

AUTO_CONNECT_PORT = 6271
AUTO_CONNECT_ADDRESS = "0.0.0.0"

SERVER_ADDRESS = "0.0.0.0"
SERVER_PORT = 7325
