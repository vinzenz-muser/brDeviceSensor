from socketio import Client
from socketio.exceptions import BadNamespaceError, ConnectionError
import yaml
import os
import time
import random
import requests
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

@sio.event(namespace="/sensor")
def update_controller(data):
    global max_min_vals
    val = float(data["value"])
    accuracy = float(data["accuracy"])
    max_min_vals[data["sensor_id"]]["min"] = val - accuracy / 2
    max_min_vals[data["sensor_id"]]["max"] =  val + accuracy / 2

url = config['hub_url'] + "/sensor?api_key=" + config["api_key"]
sensor_ids = config["sensor_ids"]

max_min_vals = {i: {"min": None, "max": None} for i in sensor_ids}

connected = False
delay = 1

while not connected:
    try:
        sio.connect(url, namespaces=['/sensor'])
        connected = True
    except ConnectionError:
        print("Connection failed, try again in 1 seconds")
        time.sleep(delay)

running = True
while running:
    try:
        start = time.time()
        data = readSensor("/sys/bus/w1/devices/28-0118685f51ff/w1_slave", sensor_ids)

        if max_min_vals[5]["max"] and max_min_vals[5]["min"]:
            if max_min_vals[5]["min"] < data[5] < max_min_vals[5]["max"]:
                requests.get("http://192.168.1.236/relay?state=1")
            else:
                requests.get("http://192.168.1.236/relay?state=0")

        sio.emit("new_data", {"data": data}, namespace="/sensor")
        end = time.time()
        duration = end - start
        waittime = max(0, delay - duration)
        time.sleep(waittime)
    except BadNamespaceError:
        print("Namespace error, probably the hub is down. Keep on trying")


sio.wait()
