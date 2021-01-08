class DefaultSensor:
    def __init__(self, id, address, controller=None, type="subtract", target=None, accuracy=None):
        self.id = id
        self.address = address
        self.controller = controller
        self.path = "/sys/bus/w1/devices/"
        self.target = target
        self.accuracy = accuracy
        self.type = type

    def __str__(self):
        return f"<DefaultSensor: id {self.id}, address: {self.address}, target {self.target}, type: {self.type}"

    def setAccuracy(self, accuracy):
        self.accuracy = accuracy

    def setTarget(self, target):
        self.target = target

    def readData(self):
        with open(self.path + self.address + "/w1_slave", "r") as f:
            ans = f.readlines()

        first_line = ans[0].replace("\n", "")
        success = first_line.split(" ")[-1] == "YES"
        current_value = None

        if success:
            data_line = ans[1].replace("\n", "")
            if data_line[:2] != "00":
                current_value = float(data_line.split("t=")[1])/1000

        return current_value

    def updateState(self):
        current_data = self.readData()
        success = False
        if self.controller and self.target and self.accuracy:
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

        return current_data, success
