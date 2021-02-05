import time

class Sensor:
    def __init__(self, config):
        self.id = config["id"]
        self.address = config["address"]
        self.controller = config["controller"]
        self.path = "/sys/bus/w1/devices/"
        self.target = config["target"]
        self.accuracy = config["accuracy"]
        self.type = config["type"]

    def __str__(self):
        return f"<DefaultSensor: id {self.id}, address: {self.address}, target {self.target}, type: {self.type}"

    def setAccuracy(self, accuracy):
        self.accuracy = accuracy

    def setTarget(self, target):
        self.target = target

    def readData(self):
        #start = time.time()
        try:
            with open(self.path + self.address + "/w1_slave", "r") as f:
                ans = f.readlines()

            first_line = ans[0].replace("\n", "")
            success = first_line.split(" ")[-1] == "YES"
            current_value = None

            if success:
                data_line = ans[1].replace("\n", "")
                if data_line[:2] != "00":
                    current_value = float(data_line.split("t=")[1])/1000

            #print(f"Reading {self.address} took {time.time() - start} seconds")

            return current_value
        except FileNotFoundError:
            return None

    def updateState(self):
        current_data = self.readData()
        #start = time.time()
        success = False
        if current_data and self.controller and self.target and self.accuracy:
            max = self.target + self.accuracy
            min = self.target - self.accuracy
            try:
                if self.type == "subtract":
                    if max < current_data:
                        self.controller.turnOn()
                    elif min > current_data:
                        self.controller.turnOff()
                elif self.type == "add":
                    if max > current_data:
                        self.controller.turnOff()
                    elif min < current_data:
                        self.controller.turnOn()
                success = True
            except Exception as e:
                pass
        #print(f"Controlling {self.address} took {time.time() - start} seconds")
        return current_data, success
