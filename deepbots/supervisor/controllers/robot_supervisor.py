from abc import abstractmethod

from deepbots.supervisor.controllers.supervisor_env import SupervisorEnv


class RobotSupervisor(SupervisorEnv):
    """
    The RobotSupervisor class implements both a robot controller and a
    supervisor RL environment. This class can be used when there is no
    need to separate the Robot from the Supervisor, or the observations of
    the robot are too big to be packaged in messages, e.g. high resolution
    images from a camera, that introduce a bottleneck and reduce
    performance significantly.

    Controllers that inherit this method *must* run on Robot nodes
    that have supervisor privileges.

    The user needs to implement the regular methods for the environment,
    reward(), get_observations(), get_default_observation, etc., from
    SupervisorEnv according to their use-case in addition to the method
    apply_action() introduced here.

    apply_action():
    (similar to use_message_data() of RobotEmitterReceiverCSV)
    This method takes an action argument and translates it to a robot
    action, e.g. motor speeds.
    Note that apply_action() is called during step().
    """
    def __init__(self, time_step=None):
        super(RobotSupervisor, self).__init__()

        if time_step is None:
            self.timestep = int(self.supervisor.getBasicTimeStep())
        else:
            self.timestep = time_step

    def get_timestep(self):
        return self.timestep

    def step(self, action):
        """
        Default step implementation that contains a Webots step conditional
        for terminating properly.

        :param action: The agent's action
        :return: tuple, (observation, reward, is_done, info)
        """
        if self.supervisor.step(self.timestep) == -1:
            exit()

        self.apply_action(action)
        return (
            self.get_observations(),
            self.get_reward(action),
            self.is_done(),
            self.get_info(),
        )

    @abstractmethod
    def apply_action(self, action):
        """
        This method should be implemented to apply whatever actions the
        action argument contains on the robot, depending on the use-case.
        This method is called by the step() method which provides the
        action argument.

        For example, if the action argument is in the form of an integer
        value, *0* could mean the action *move forward*. In this case,
        motor speeds should be set here accordingly so the robot moves
        forward.

        :param action: list, containing action data
        """
        pass
