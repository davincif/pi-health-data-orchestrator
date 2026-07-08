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
