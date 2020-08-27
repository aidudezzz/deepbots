from abc import abstractmethod

from deepbots.supervisor.controllers.supervisor_env import SupervisorEnv


class RobotSupervisor(SupervisorEnv):
    """
    The RobotSupervisor class implements both a robot controller and a supervisor RL environment.
    This class can be used when there is no need to separate the Robot from the Supervisor, or
    the observations of the robot are too big to be packaged in messages, e.g. high resolution
    images from a camera, that introduce a bottleneck and reduce performance significantly.

    Reset method
    This class contains a default implementation of reset() that uses Webots-provided methods to reset
    the world to its starting state.
    *Note that this works properly only with Webots versions >R2020b and must be
    overridden with a custom reset method when using earlier versions. It is backwards compatible
    due to the fact that the new reset method gets overridden by whatever the user has previously
    implemented, so an old supervisor such as SupervisorCSV can be migrated easily to use this class.

    The user needs to implement the regular methods (reward(), get_observations(), etc.) from
    SupervisorEnv according to their use-case in addition to the methods get_default_observation()
    and apply_action() introduced here.

    get_default_observation():
    This method should be implemented to return a per use-case default observation that is used when resetting.

    apply_action():
    (similar to use_message_data() of RobotEmitterReceiverCSV)
    This method takes an action argument and translates it to a robot action, e.g. motor speeds.
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
        Default step implementation that contains a Webots step conditional for
        terminating properly.

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

        :param action: list, containing action data
        """
        pass
