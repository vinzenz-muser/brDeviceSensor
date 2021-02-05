import controllers.Interface as Interface
import requests

class Controller(Interface.ControllerInterface):
    def __init__(self, settings):
        pass
    def __str__(self):
        return f"<SkipController: ip: {self.ip}>"

    def turnOn(self):
        pass

    def turnOff(self):
        pass
