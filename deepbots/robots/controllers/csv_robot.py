from collections.abc import Iterable

from deepbots.robots.controllers.emitter_receiver_robot import \
    EmitterReceiverRobot


class CSVRobot(EmitterReceiverRobot):
    """
    Basic implementation of a robot that can emit and receive messages to/from
    the supervisor in string utf-8 form that are Comma Separated Values,
    i.e. a list.
    """
    def __init__(self,
                 emitter_name="emitter",
                 receiver_name="receiver",
                 timestep=None):
        """
        The constructor just passes the arguments provided to the parent
        class contructor.

        :param emitter_name: The name of the emitter device on the
            robot node, defaults to "emitter"
        :param receiver_name: The name of the receiver device on the
            robot node, defaults to "receiver"
        :param timestep: The robot controller timestep, defaults to None
        """
        super().__init__(emitter_name, receiver_name, timestep)

    def initialize_comms(self, emitter_name, receiver_name):
        """
        This method implements the basic emitter/receiver initialization that
        assumes that an emitter and a receiver component are present on the
        Webots robot with appropriate DEFs ("emitter"/"receiver").

        :param emitter_name: The name of the emitter device on the
            supervisor node
        :param receiver_name: The name of the receiver device on the
            supervisor node
        :return: The initialized emitter and receiver references
        """
        emitter = self.getDevice(emitter_name)
        receiver = self.getDevice(receiver_name)
        receiver.enable(self.timestep)
        return emitter, receiver

    def handle_emitter(self):
        """
        This emitter uses the user-implemented create_message() method to get
        whatever data the robot gathered, convert it to a string if needed and
        then use the emitter to send the data in a string utf-8 encoding to the
        supervisor.
        """
        data = self.create_message()

        assert isinstance(data,
                          Iterable), "The action object should be Iterable"

        string_message = ""
        # message can either be a list that needs to be converted in a string
        # or a straight-up string
        if type(data) is list:
            string_message = ",".join(map(str, data))
        elif type(data) is str:
            string_message = data
        else:
            raise TypeError(
                "message must be either a comma-separated string or a 1D list")

        string_message = string_message.encode("utf-8")
        self.emitter.send(string_message)

    def handle_receiver(self):
        """
        This receiver uses the basic Webots receiver-handling code. The
        use_message_data() method should be implemented to actually use the
        data received from the supervisor.
        """
        if self.receiver.getQueueLength() > 0:
            # Receive and decode message from supervisor
            try:
                message = self.receiver.getString()
            except AttributeError:
                message = self.receiver.getData().decode("utf-8")
            # Convert string message into a list
            message = message.split(",")

            self.use_message_data(message)

            self.receiver.nextPacket()

    def create_message(self):
        """
        This method should be implemented to convert whatever data the robot
        has, eg. sensor data, into a message to be sent to the supervisor via
        the emitter.

        :return: a list or a comma-separated string containing all data
        """
        raise NotImplementedError

    def use_message_data(self, message):
        """
        This method should be implemented to apply whatever actions the
        message (received from the supervisor) contains.

        :param message: list containing data received from the supervisor
        """
        raise NotImplementedError
