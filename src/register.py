import controllers.MyStrom
import controllers.NoController
import sensors.DefaultSensor
import sensors.RandomSensor

controllers = {
    "mystrom": controllers.MyStrom.Controller,
    "none": controllers.NoController.Controller
}

sensors = {
    "default": sensors.DefaultSensor.Sensor,
    "random": sensors.RandomSensor.Sensor
}
