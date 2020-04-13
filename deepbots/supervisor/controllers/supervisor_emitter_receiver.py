from abc import abstractmethod
from collections.abc import Iterable

from controller import Supervisor

from .supervisor_env import SupervisorEnv


class SupervisorEmitterReceiver(SupervisorEnv):
    def __init__(self,
                 emitter_name="emitter",
                 receiver_name="receiver",
                 time_step=None):

        super(SupervisorEmitterReceiver, self).__init__()

        self.supervisor = Supervisor()

        if time_step is None:
            self.timestep = int(self.supervisor.getBasicTimeStep())
        else:
            self.timestep = time_step

        self.initialize_comms(emitter_name, receiver_name)

    def initialize_comms(self, emitter_name, receiver_name):
        self.emitter = self.supervisor.getEmitter(emitter_name)
        self.receiver = self.supervisor.getReceiver(receiver_name)
        self.receiver.enable(self.timestep)
        return self.emitter, self.receiver

    def step(self, action):
        self.supervisor.step(self.timestep)

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

        self._last_message = None

    def handle_emitter(self, action):
        assert isinstance(action, Iterable), \
            "The action object should be Iterable"

        message = (",".join(map(str, action))).encode("utf-8")
        self.emitter.send(message)

    def handle_receiver(self):
        if self.receiver.getQueueLength() > 0:
            string_message = self.receiver.getData().decode("utf-8")
            self._last_message = string_message.split(",")

            self.receiver.nextPacket()

        return self._last_message
