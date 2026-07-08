import os

from database.client_manager import ClientManager

kill_now = False
version = "0.0.2"
verbose = False
DB_PATH = os.getenv("DB_PATH", "./data/")

update_rate = 0.9
db_back_rate = 1 * 60 * 60
# read_for_new_connetion_lock = threading.Lock()

client_manager = ClientManager({"db_addrs": "db.sqlite3"})

SERVER_ADDRESS = "0.0.0.0"
SERVER_PORT = 7325
