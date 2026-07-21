# PI Health Data Orchestrator

## run

```sh
pip install requeriments.txt
python3 main.py
```

## Docker

```sh
sudo docker build --network=host -t ldavincif/pi-health-data-orchestrator .
sudo docker run -d -p 0.0.0.0:6271:6271 -p 0.0.0.0:7325:7325 --name pi-health-data-orchestrator ldavincif/pi-health-data-orchestrator

# sudo docker build --network=host -t ldavincif/ldavincif-portal . && sudo docker stop $(sudo docker ps -aq) && sudo docker rm $(sudo docker ps -aq) && sudo docker run -d -p 0.0.0.0:8080:8080/tcp --name ldavincif-portal-1 ldavincif/ldavincif-portal
```

<!--
ClientManager
Sleeping for 42379.493227 seconds until 2026-07-19 00:00:00...
self.db <database.sqlite_impl.SQLiteImpl object at 0x7850e81cf830>
raspbarry-health-data-collector version: 0.0.2
by - davincif
check me @ ldavincif.com

WebSocket Server started @ 0.0.0.0:7325
WebSocket online.
update_device
device_info {'requester': 'davincif-ThinkPad', 'command': 'update-unmutable', 'uptime': {'bt': 1784363163.0}, 'process': {'cr': 8, 'lcr': 16, 'mnf': 800.0, 'mxf': 4800.0, 'lcrinfo': [{'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}, {'mnf': 800.0, 'mxf': 4800.0}]}, 'memory': {'v': {'t': 67114721280}, 's': {'t': 0}}, 'disk': {'t': 411281928192, 'u': 249575415808, 'f': 140739637248, 'p': 63.9}, 'now': 10054.55689741}
^Csignal SIGINT received, closing...
WebSocket Server closed.
keepalive ping failed
TimeoutError: timed out while closing connection

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/davincif/Documents/Projects/pi-health-data-orchestrator/venv/lib/python3.12/site-packages/websockets/sync/connection.py", line 784, in keepalive
    with self.send_context():
  File "/usr/lib/python3.12/contextlib.py", line 144, in __exit__
    next(self.gen)
  File "/home/davincif/Documents/Projects/pi-health-data-orchestrator/venv/lib/python3.12/site-packages/websockets/sync/connection.py", line 1020, in send_context
    raise self.protocol.close_exc from original_exc
websockets.exceptions.ConnectionClosedError: sent 1011 (internal error) keepalive ping timeout; no close frame received
__renewal
-->
