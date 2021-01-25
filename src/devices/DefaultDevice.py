from joblib import Parallel, delayed
from helpers import setup
import json
import time


class DefaultDevice:
    def __init__(self):
        self.sensors = {}
        self.n_jobs = 1
        return

    def load_from_config(self, config):
        self.sensors = setup.get_sensors_from_config(config)
        self.n_jobs = len(self.sensors)

    def set_targets(self, data):
        target = float(data["value"])
        accuracy = float(data["accuracy"])
        sensor_id = int(data["sensor_id"])
        self.sensors[sensor_id].setTarget(target)
        self.sensors[sensor_id].setAccuracy(accuracy)

        lastval = {sensor.id: {'target': sensor.target, 'accuracy': sensor.accuracy} for _, sensor in self.sensors.items()}

        with open('src/fallback/controller_data.json', 'w') as f:
            json.dump(lastval, f)

        return

    def get_sensor_targets(self, sensor_id=None):
        if sensor_id is None:
            return [{'sensor_id': sensor.id, 'value': sensor.target, 'accuracy': sensor.accuracy} for id, sensor in self.sensors.items()]
        else:
            try:
                sensor = self.sensors[sensor_id]
                data = {'sensor_id': sensor.id, 'value': sensor.target, 'accuracy': sensor.accuracy}
                return [data]
            except KeyError:
                return {}

    def _update_sensor_state(self, id):
        data, success = self.sensors[id].updateState()
        return id, data

    def get_sensor_values(self):
        ans = Parallel(self.n_jobs)(delayed(self._update_sensor_state)(id) for id, _ in self.sensors.items())

        return {i[0]: i[1] for i in ans}
