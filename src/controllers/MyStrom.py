import controllers.Interface as Interface
import requests

class Controller(Interface.ControllerInterface):
    def __init__(self, settings):
        self.ip = settings["ip"]

    def on(self):
        conn_string = f"http://{self.ip}/relay?state=1"
        requests.get(conn_string)

    def off(self):
        conn_string = f"http://{self.ip}/relay?state=0"
        requests.get(conn_string)
