from abc import ABC, abstractmethod


class SupervisorEnv(ABC):
    @abstractmethod
    def get_observations(self):
        pass

    @abstractmethod
    def step(self, action):
        pass

    @abstractmethod
    def get_reward(self, action):
        pass

    @abstractmethod
    def is_done(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_info(self):
        pass
