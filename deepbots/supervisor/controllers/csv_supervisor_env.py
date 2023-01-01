from collections.abc import Iterable

from deepbots.supervisor.controllers.emitter_receiver_supervisor_env import \
    EmitterReceiverSupervisorEnv


class CSVSupervisorEnv(EmitterReceiverSupervisorEnv):
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
        super(CSVSupervisorEnv, self).__init__(emitter_name, receiver_name,
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
