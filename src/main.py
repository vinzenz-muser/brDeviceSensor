from socketio import Client
from socketio.exceptions import BadNamespaceError, ConnectionError
import yaml
import os
import time
import random
import requests
from controllers_register import controllers as configured_controllers
from helpers import setup

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
    target = float(data["value"])
    accuracy = float(data["accuracy"])
    sensor_id = int(data["sensor_id"])
    sensors[sensor_id].setTarget(target)
    sensors[sensor_id].setAccuracy(accuracy)

url = config['hub_url'] + "/sensor?api_key=" + config["api_key"]
sensors = setup.get_sensors_from_config(config)

connected = False
delay = 1

while True:
    if not connected:
        try:
            sio.connect(url, namespaces=['/sensor'])
            connected = True
        except ConnectionError:
            print("Connection failed, try again after delay")
            connected = False

    try:
        start = time.time()
        data = dict()

        for id, sensor in sensors.items():
            data[id], update_state = sensor.updateState()

        if connected:
            sio.emit("new_data", {"data": data}, namespace="/sensor")

        end = time.time()
        duration = end - start
        print(duration)
        waittime = max(0, delay - duration)
        time.sleep(waittime)

    except BadNamespaceError:
        connected = False
        print("Namespace error, probably the hub is down. Keep on trying")


#sio.wait()
