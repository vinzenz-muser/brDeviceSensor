# brDeviceSensor

Implementation of a device that can be used for https://github.com/vinzenz-muser/brControl. 

To run a default device with two random sensors, you can use the following config:

```
api_key: <api-key>
hub_url: http://localhost:5000/
sensors:
  - id: 1
    type: random
    controller: none
    address: ""
    settings:
  - id: 2
    type: random
    controller: none
    address: ""
    settings:


```

Where you have to adapt the `api_key` accordingly. You can find the key in the Admin-Panel of the brControl-App. If you started the server on a different url, you'll have to adapt this as well. 

Once you have followed the steps to start a `brControl` Server, follow these steps to run a device with random sensors. Please make sure that you added a device in the admin panel before you start it.

1. (Optional) Start and initialize a virtual environment with `python -m vevn venv && source venv/bin/activate`
2. Install requirements: `pip install -r requirements.txt`
3. Save example config from above as `config.yaml` and adapt the api-key, url, and ids of the sensors if necessary
4. Start the sensor with `python src/main.py`

This implementation was done for a Raspberry Pi Zero paired with a set of DS18B20 temperature sensors. 

To use the same setup, change the `type` of the sensors to `default` and change the `adress` to the device adresses. If you need help to setup the raspberry pi, you can follow this tutorial: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview.

This implementation will use `joblib.Parallel` to run the reading-operations in parallel, so adding more sensors is not an issue up to a certain degree.

The Controller that is currently implemented is based on the MyStrom-API for the MyStrom-Switches (https://mystrom.ch/). In order to use those controllers, assign a fixed IP to them and add this IP in the settings of the corresponding sensor.