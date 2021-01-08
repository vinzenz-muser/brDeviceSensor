from sensors.DefaultSensor import DefaultSensor
from controllers_register import controllers

def get_sensors_from_config(config):
    sensor_configs = config["sensors"]
    sensors = dict()

    for config in sensor_configs:
        controller_class = controllers[config["type"]]

        sensors[config["id"]] = DefaultSensor(
            id = config["id"],
            address = config["address"],
            controller = controller_class(config["settings"])
        )

    return sensors
