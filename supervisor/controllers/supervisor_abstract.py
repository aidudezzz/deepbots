import sys
from abc import ABC, abstractmethod

# from controller import Supervisor

class AbstractSupervisor(SupervisorEnv, ABC):
    def __init__(self, timestep=None):
        self.supervisor = Supervisor()

        if timestep is None:
            self.timestep = self.supervisor.getBasicTimeStep()
        else:
            self.timestep = timestep

    def step(self, action):
        self.supervisor.step(self.timestep)

        self.do_action(action)
        return self.get_observations(), self.get_reward(action),\
            self.is_done(), self.get_info()

    @abstractmethod
    def do_action(self, action):
        pass
