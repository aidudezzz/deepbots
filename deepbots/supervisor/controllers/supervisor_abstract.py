from abc import ABC, abstractmethod

from controller import Supervisor

from deepbots.supervisor.controllers.supervisor_env import SupervisorEnv


class SupervisorAbstract(SupervisorEnv, ABC):
    def __init__(self, timestep=None):
        super(SupervisorAbstract, self).__init__()
        self.supervisor = Supervisor()

        if timestep is None:
            self.timestep = int(self.supervisor.getBasicTimeStep())
        else:
            self.timestep = timestep

    def step(self, action):
        self.supervisor.step(self.timestep)

        self.do_action(action)
        return (
            self.get_observations(),
            self.get_reward(action),
            self.is_done(),
            self.get_info(),
        )

    def get_timestep(self):
        return self.timestep

    @abstractmethod
    def do_action(self, action):
        pass
