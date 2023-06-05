import json
import register


def get_sensors_from_config(config):
    sensor_configs = config["sensors"]
    sensors = dict()

    for config in sensor_configs:
        controller_class = register.controllers[config["controller"]]
        sensor_class = register.sensors[config["type"]]
        sensors[config["id"]] = sensor_class(
            dict(
                id=config["id"],
                address=config["address"],
                controller=controller_class(config["settings"]),
            )
        )

    try:
        with open("src/fallback/controller_data.json", "r") as f:
            controller_data = json.load(f)
        for id, con in controller_data.items():
            sensors[int(id)].setTarget(con["target"])
            sensors[int(id)].setAccuracy(con["accuracy"])
    except FileNotFoundError:
        print("No fallback data found, starting with Nones.")

    return sensors
