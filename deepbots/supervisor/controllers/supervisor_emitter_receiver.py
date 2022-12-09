from collections.abc import Iterable
from warnings import warn, simplefilter

from deepbots.supervisor.controllers.supervisor_env import SupervisorEnv
from controller import Supervisor


class SupervisorEmitterReceiver(SupervisorEnv):
    """
    This is the base class for the emitter - receiver scheme.

    Subclasses implement a variety of communication formats such as CSV
    messages.
    """
    def __init__(self,
                 emitter_name="emitter",
                 receiver_name="receiver",
                 timestep=None):
        """
        The constructor sets up the timestep and calls the method that
        initializes the emitter and receiver devices with the names provided.

        :param emitter_name: The name of the emitter device on the
            supervisor node
        :param receiver_name: The name of the receiver device on the
            supervisor node
        :param timestep: The supervisor controller timestep
        """
        super(SupervisorEmitterReceiver, self).__init__()

        if timestep is None:
            self.timestep = int(self.getBasicTimeStep())
        else:
            self.timestep = timestep

        self.emitter, self.receiver = self.initialize_comms(
            emitter_name, receiver_name)

    def initialize_comms(self, emitter_name, receiver_name):
        """
        Initializes the emitter and receiver devices with the names provided.

        :param emitter_name: The name of the emitter device on the
            supervisor node
        :param receiver_name: The name of the receiver device on the
            supervisor node
        :return: The initialized emitter and receiver references
        """
        emitter = self.getEmitter(emitter_name)
        receiver = self.getReceiver(receiver_name)
        receiver.enable(self.timestep)
        return emitter, receiver

    def step(self, action):
        """
        The basic step method that steps the controller,
        calls the method that sends the action through the emitter
        and returns the (observations, reward, done, info) object.

        :param action: Whatever the use-case uses as an action, e.g.
            an integer representing discrete actions
        :type action: Defined by the implementation of handle_emitter
        :return: (observations, reward, done, info) as provided by the
            corresponding methods as implemented for the use-case
        """
        self.handle_emitter(action)
        if super(Supervisor, self).step(self.timestep) == -1:
            exit()

        return (
            self.get_observations(),
            self.get_reward(action),
            self.is_done(),
            self.get_info(),
        )

    def handle_emitter(self, action):
        """
        This method is implemented by subclasses depending on the
        communication format used.

        :param action: The action that is sent through the emitter device
            to the robot, e.g. an integer representing discrete actions
        """
        raise NotImplementedError

    def handle_receiver(self):
        """
        This method is implemented by subclasses depending on the
        communication format used.
        """
        raise NotImplementedError

    def get_timestep(self):
        # The filter is required so as to not ignore the Deprecation warning
        simplefilter("once")
        warn("get_timestep is deprecated, use .timestep instead",
                  DeprecationWarning)
        return self.timestep

    @property
    def timestep(self):
        """
        Getter of _timestep field. Timestep is defined in milliseconds

        :return: The timestep of the controller in milliseconds
        """
        return self._timestep

    @timestep.setter
    def timestep(self, value):
        """
        Setter of timestep field. Automatically converts to int as
        required by Webots.

        :param value: The new controller timestep in milliseconds
        """
        self._timestep = int(value)


class SupervisorCSV(SupervisorEmitterReceiver):
    """
    This class implements the emitter-receiver scheme using Comma Separated
    Values.
    """
    def __init__(self,
                 emitter_name="emitter",
                 receiver_name="receiver",
                 timestep=None):
        """
        The constructor just passes the arguments provided to the parent
        class contructor.

        :param emitter_name: The name of the emitter device on the
            supervisor node
        :param receiver_name: The name of the receiver device on the
            supervisor node
        :param timestep: The supervisor controller timestep
        """
        super(SupervisorCSV, self).__init__(emitter_name, receiver_name,
                                            timestep)

    def handle_emitter(self, action):
        """
        Implementation of the handle_emitter method expecting an iterable
        with Comma Separated Values (CSV).

        :param action: Whatever the use-case uses as an action, e.g.
            an integer representing discrete actions
        :type action:  Iterable, for multiple values the CSV format is
            required, e.g. [0, 1] for two actions
        """
        assert isinstance(action, Iterable), \
            "The action object should be Iterable"

        message = (",".join(map(str, action))).encode("utf-8")
        self.emitter.send(message)

    def handle_receiver(self):
        """
        Implementation of the handle_receiver method expecting an iterable
        with Comma Separated Values (CSV).

        :return: Returns the message received from the robot, returns None
            if no message is received
        :rtype: List of string values
        """
        if self.receiver.getQueueLength() > 0:
            try:
                string_message = self.receiver.getString()
            except AttributeError:
                string_message = self.receiver.getData().decode("utf-8")
            self.receiver.nextPacket()
            return string_message.split(",")
        else:
            return None
