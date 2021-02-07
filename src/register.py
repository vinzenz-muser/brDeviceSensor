import controllers.MyStrom, controllers.NoController
import sensors.DefaultSensor, sensors.RandomSensor

controllers = {
    "mystrom": controllers.MyStrom.Controller,
    "none": controllers.NoController.Controller
}

sensors = {
    "default": sensors.DefaultSensor.Sensor,
    "random": sensors.RandomSensor.Sensor
}
