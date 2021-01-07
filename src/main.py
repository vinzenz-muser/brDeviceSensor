from socketio import Client
from socketio.exceptions import BadNamespaceError, ConnectionError
import yaml
import os
import time
import random
import requests
from sensors import readSensor
from controllers_register import controllers as configured_controllers

with open(r'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

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
sensor_configs = config["sensors"]

sensors = dict()

for config in sensor_configs:
    controller_class = configured_controllers[config["type"]]
    sensors[config["id"]] = {
        "id": config["id"],
        "controller": controller_class(config["settings"]),
        "max": None,
        "min": None
    }

connected = False
delay = 1

while not connected:
    try:
        sio.connect(url, namespaces=['/sensor'])
        connected = True
    except ConnectionError:
        print("Connection failed, try again in 1 seconds")
        time.sleep(delay)

running = False
while running:
    try:
        start = time.time()
        data = readSensor("/sys/bus/w1/devices/28-0118685f51ff/w1_slave", sensor_ids)
        print(max_min_vals)
        try:
            if max_min_vals[5]["max"] and max_min_vals[5]["min"]:
                if max_min_vals[5]["min"] < data[5] < max_min_vals[5]["max"]:
                    requests.get("http://192.168.1.236/relay?state=1")
                else:
                    requests.get("http://192.168.1.236/relay?state=0")

        except KeyError:
            pass
        sio.emit("new_data", {"data": data}, namespace="/sensor")
        end = time.time()
        duration = end - start
        waittime = max(0, delay - duration)
        time.sleep(waittime)
    except BadNamespaceError:
        print("Namespace error, probably the hub is down. Keep on trying")


sio.wait()
