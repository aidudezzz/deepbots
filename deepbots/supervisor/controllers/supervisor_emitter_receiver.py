from abc import abstractmethod
from collections.abc import Iterable

from .supervisor_env import SupervisorEnv


class SupervisorEmitterReceiver(SupervisorEnv):
    def __init__(self,
                 emitter_name="emitter",
                 receiver_name="receiver",
                 time_step=None):

        super(SupervisorEmitterReceiver, self).__init__()

        if time_step is None:
            self.timestep = int(self.supervisor.getBasicTimeStep())
        else:
            self.timestep = time_step

        self.emitter = None
        self.receiver = None
        self.initialize_comms(emitter_name, receiver_name)

    def initialize_comms(self, emitter_name, receiver_name):
        self.emitter = self.supervisor.getEmitter(emitter_name)
        self.receiver = self.supervisor.getReceiver(receiver_name)
        self.receiver.enable(self.timestep)
        return self.emitter, self.receiver

    def step(self, action):
        if self.supervisor.step(self.timestep) == -1:
            exit()

        self.handle_emitter(action)
        return (
            self.get_observations(),
            self.get_reward(action),
            self.is_done(),
            self.get_info(),
        )

    @abstractmethod
    def handle_emitter(self, action):
        pass

    @abstractmethod
    def handle_receiver(self):
        pass

    def get_timestep(self):
        return self.timestep


class SupervisorCSV(SupervisorEmitterReceiver):
    def __init__(self,
                 emitter_name="emitter",
                 receiver_name="receiver",
                 time_step=None):
        super(SupervisorCSV, self).__init__(emitter_name, receiver_name,
                                            time_step)

    def handle_emitter(self, action):
        assert isinstance(action, Iterable), \
            "The action object should be Iterable"

        message = (",".join(map(str, action))).encode("utf-8")
        self.emitter.send(message)

    def handle_receiver(self):
        if self.receiver.getQueueLength() > 0:
            string_message = self.receiver.getData().decode("utf-8")
            self.receiver.nextPacket()
            return string_message.split(",")
        else:
            return None
