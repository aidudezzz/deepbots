from abc import ABC, abstractmethod

from controller import Robot


class RobotEmmiterReceiver(ABC):
    def __init__(self, timestep=None):
        self.robot = Robot()

        if timestep is None:
            self.timestep = int(self.robot.getBasicTimeStep())
        else:
            self.timestep = timestep

    @abstractmethod
    def handleEmitter():
        pass

    @abstractmethod
    def handleReceiver(self):
        pass

    def run(self):
        while self.robot.step(self.timestep) != -1:
            self.handleReceiver()
            self.handleEmitter()
