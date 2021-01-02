import socketio
import yaml
import os
import time
import random
from sensors import readSensor

with open(r'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    print(config)

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

url = config['hub_url'] + "/sensor?api_key=" + config["api_key"]
sensor_ids = config["sensor_ids"]
print(sensor_ids)
sio.connect(url, namespaces=['/sensor'])

delay = 1

while True:
    start = time.time()

    data = readSensor("/sys/bus/w1/devices/28-0118685f51ff/w1_slave", sensor_ids)
    sio.emit("new_data", {"Data": data}, namespace="/sensor")

    end = time.time()
    duration = end - start
    waittime = max(0, delay - duration)
    time.sleep(waittime)
