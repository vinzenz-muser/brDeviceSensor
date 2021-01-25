from socketio import Client
from socketio.exceptions import BadNamespaceError, ConnectionError
import yaml
import os
import time
import random
import requests
import json
from controllers_register import controllers as configured_controllers
from devices.DefaultDevice import DefaultDevice
from helpers import setup
from queue import Queue
import threading


with open(r'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

sio = Client()

@sio.event(namespace='/sensor')
def connect():
    print('connection established')
    update_targets_on_server()

@sio.event
def disconnect():
    print('disconnected from server')

@sio.event(namespace="/sensor")
def update_controller(data):
    print("Got data from hub: ", data)
    set_targets(data)

def set_targets(data):
    device.set_targets(data)
    update_targets_on_server(data["sensor_id"])

def update_targets_on_server(sensor_id = None):
    ans = device.get_sensor_targets(sensor_id)
    sio.emit("updated_targets", ans, namespace="/sensor")


url = config['hub_url'] + "/sensor?api_key=" + config["api_key"]

connected = False
delay = 1

device = DefaultDevice()
device.load_from_config(config)

while True:
    if not connected:
        try:
            sio.connect(url, namespaces=['/sensor'])
            connected = True
        except ConnectionError:
            print(f"Connection to {url} failed, t   ry again after delay")
            connected = False

    try:
        start = time.time()
        data = device.get_sensor_values()

        if connected:
            sio.emit("new_data", {"data": data}, namespace="/sensor")

        end = time.time()
        duration = end - start
        waittime = max(0, delay - duration)
        time.sleep(waittime)

    except BadNamespaceError:
        print("Namespace error, probably the hub is down. Keep on trying")


#sio.wait()
