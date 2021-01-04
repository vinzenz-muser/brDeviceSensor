from socketio import Client
from socketio.exceptions import BadNamespaceError, ConnectionError
import yaml
import os
import time
import random
from sensors import readSensor

with open(r'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    print(config)

sio = Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

url = config['hub_url'] + "/sensor?api_key=" + config["api_key"]
sensor_ids = config["sensor_ids"]

connected = False
delay = 1

while not connected:
    try:
        sio.connect(url, namespaces=['/sensor'])
        connected = True
    except ConnectionError:
        print("Connection failed, try again in 1 seconds")
        time.sleep(delay)

while True:
    try:
        start = time.time()
        data = readSensor("/sys/bus/w1/devices/28-0118685f51ff/w1_slave", sensor_ids)
        print("sending data ", data)
        sio.emit("new_data", {"data": data}, namespace="/sensor")
        end = time.time()
        duration = end - start
        waittime = max(0, delay - duration)
        time.sleep(waittime)
    except BadNamespaceError:
        print("Namespace error, probably the hub is down. Keep on trying")
