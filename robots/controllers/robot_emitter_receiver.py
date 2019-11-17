# from deepbots.robots.robot_controller import RobotController
from .robot_controller import RobotController
from abc import abstractmethod


class RobotEmitterReceiver(RobotController):
    """
    Basic implementation of a robot that can emit and receive messages to/from the supervisor in string utf-8 form
    that are comma separated.
    """
    def __init__(self, timestep=None):
        super().__init__(timestep=timestep)

    def initialize_comms(self):
        """
        This method implements the basic emitter/receiver initialization that assumes that an emitter and a receiver
        components are present on the Webots robot with appropriate DEFs ("emitter"/"receiver").
        :return: emitter and receiver references
        """
        emitter = self.robot.getEmitter("emitter")
        receiver = self.robot.getReceiver("receiver")
        receiver.enable(self.timestep)
        return emitter, receiver

    def handle_emitter(self):
        """
        This emitter uses the user-implemented get_robot_data() method to get whatever data the robot gathered,
        convert it to a string if needed and then use the emitter to send the data in a string utf-8 encoding to the
        supervisor.
        """
        data = self.get_robot_data()

        string_message = ""
        # message can either be a list that needs to be converted in a string or a straight-up string
        if type(data) is list:
            for i in range(len(data)):
                string_message += data[i] + ","
        elif type(data) is str:
            string_message = data
        else:
            raise TypeError("message must be either a comma-separated string or a 1D list")

        string_message = string_message.encode('utf-8')
        self.emitter.send(string_message)

    def handle_receiver(self):
        """
        This receiver uses the basic Webots receiver-handling code. The use_message_data() method should be implemented
        to actually use the data received from the supervisor.
        """
        if self.receiver.getQueueLength() > 0:
            # Receive and decode message from supervisor
            message = self.receiver.getData().decode('utf-8')
            # Convert string message into a list
            message = message.split(',')

            self.use_message_data(message)

            self.receiver.nextPacket()

    @abstractmethod
    def get_robot_data(self):
        """
        This method should be implemented to convert whatever data the robot has, eg. sensor data, into a message to be
        sent to the supervisor via the emitter.
        :return: a list or a comma-separated string containing all data
        """
        pass

    @abstractmethod
    def use_message_data(self, message):
        """
        This method should be implemented to apply whatever actions the message (received from the supervisor) contains.
        :param message: list containing data received from the supervisor
        """
        pass
