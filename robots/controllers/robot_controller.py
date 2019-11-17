from abc import ABC, abstractmethod

from controller import Robot


class RobotController(ABC):
    def __init__(self, timestep=None):
        self.robot = Robot()

        if timestep is None:
            self.timestep = int(self.robot.getBasicTimeStep())
        else:
            self.timestep = timestep

    @abstractmethod
    def handle_emitter(self):
        pass

    @abstractmethod
    def handle_receiver(self):
        pass

    def run(self):
        while self.robot.step(self.timestep) != -1:
            self.handle_receiver()
            self.handle_emitter()
