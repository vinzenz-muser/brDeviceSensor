import time
import random

class Sensor:
    def __init__(self, config):
        self.id = config["id"]
        self.accuracy = None
        self.target = None

    def __str__(self):
        return f"<RandomSensor: id {self.id}, address: {self.address}, target {self.target}, type: {self.type}"

    def setAccuracy(self, accuracy):
        self.accuracy = accuracy

    def setTarget(self, target):
        self.target = target

    def readData(self):
        if self.target and self.accuracy:
            ans = random.random() * self.accuracy - 1/2*self.accuracy + self.target
        else:
            ans = 100*random.random()
        return ans

    def updateState(self):
        current_data = self.readData()
        success = True
        return current_data, success
