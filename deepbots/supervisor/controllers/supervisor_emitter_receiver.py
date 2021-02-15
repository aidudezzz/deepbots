from collections.abc import Iterable

from .supervisor_env import SupervisorEnv


class SupervisorEmitterReceiver(SupervisorEnv):
    """
    This is the base class for the emitter - receiver scheme.

    Subclasses implement a variety of communication formats such as CSV
    messages.
    """
    def __init__(self, emitter_name="emitter", receiver_name="receiver",
                 time_step=None):
        """
        The constructor sets up the time_step and calls the method that
        initializes the emitter and receiver devices with the names provided.

        :param emitter_name: The name of the emitter device on the
            supervisor node
        :param receiver_name: The name of the receiver device on the
            supervisor node
        :param time_step: The supervisor controller timestep
        """
        super(SupervisorEmitterReceiver, self).__init__()

        if time_step is None:
            self.timestep = int(self.getBasicTimeStep())
        else:
            self.timestep = time_step

        self.emitter, self.receiver = self.initialize_comms(
            emitter_name, receiver_name)

    def initialize_comms(self, emitter_name, receiver_name):
        """
        Initializes the emitter and receiver devices with the names provided.

        :param emitter_name: The name of the emitter device on the
            supervisor node
        :param receiver_name: The name of the receiver device on the
            supervisor node
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
        if self.step(self.timestep) == -1:
            exit()

        self.handle_emitter(action)
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
        # TODO maybe remove this altogether and make self.timestep
        #  a pythonic class property. Print deprecation warning for
        #  next version?
        return self.timestep


class SupervisorCSV(SupervisorEmitterReceiver):
    """
    This class implements the emitter-receiver scheme using Comma Separated
    Values.
    """
    def __init__(self, emitter_name="emitter", receiver_name="receiver",
                 time_step=None):
        """
        The constructor just passes the arguments provided to the parent
        class contructor.

        :param emitter_name: The name of the emitter device on the
            supervisor node
        :param receiver_name: The name of the receiver device on the
            supervisor node
        :param time_step: The supervisor controller timestep
        """
        super(SupervisorCSV, self).__init__(emitter_name, receiver_name,
                                            time_step)

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
            string_message = self.receiver.getData().decode("utf-8")
            self.receiver.nextPacket()
            return string_message.split(",")
        else:
            return None
