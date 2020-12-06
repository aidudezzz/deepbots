from abc import ABC, abstractmethod

from controller import Supervisor


class SupervisorEnv(ABC):
    """
    This class represents the basic template which contains the necessary
    methods to train a reinforcement learning algorithm. The interface class
    follows the gym interface which is standardized in many reinforcement
    learning algorithms. The OpenAI gym environment can be described by the
    following figure:

    +----------+             (action)            +---------------+
    |          |-------------------------------->|               |
    |   Agent  |                                 | SupervisorEnv |
    |          |<--------------------------------|               |
    +----------+      (observation, reward)      +---------------+

    This class is not intended for user usage, but to provide a common
    interface for all provided supervisor classes and make them
    compatible with reinforcement learning agents that work with
    the gym interface. Moreover, a problem-agnostic reset method is
    provided. Please use any of the children supervisor  classes to be
    inherited by your own classes, such as the RobotSupervisor class.
    Nevertheless, advanced users can inherit this class to create
    their own supervisor classes if they wish.
    """

    def __init__(self):
        self.supervisor = Supervisor()

    @abstractmethod
    def get_observations(self):
        """
        Return the observations of the robot. For example, metrics from
        sensors, a camera image, etc.

        :returns: An object of observations
        """
        pass

    @abstractmethod
    def step(self, action):
        """
        On each timestep, the agent chooses an action for the previous
        observation, *state_t*, and the environment returns the next
        observation, *state_t+1*, the reward and whether the episode
        is done or not.

        observation: The next observation from the environment
        reward: The amount of reward awarded on this step
        is_done: Whether the episode is done
        info: Diagnostic information mostly useful for debugging.

        :param action: The agent's action
        :return: tuple, (observation, reward, is_done, info)
        """
        pass

    @abstractmethod
    def get_reward(self, action):
        """
        Calculates and returns the reward for this step.

        :param action: The agent's action
        :return: The amount of reward awarded on this step
        """
        pass

    @abstractmethod
    def is_done(self):
        """
        Used to inform the agent that the problem is solved.

        :return: bool, True if the episode is done
        """
        pass

    def reset(self):
        """
        Used to reset the world to an initial state.

        Default, problem-agnostic, implementation of reset method,
        using Webots-provided methods.

        *Note that this works properly only with Webots versions >R2020b
        and must be overridden with a custom reset method when using
        earlier versions. It is backwards compatible due to the fact
        that the new reset method gets overridden by whatever the user
        has previously implemented, so an old supervisor can be migrated
        easily to use this class.

        :return: default observation provided by get_default_observation()
        """
        self.supervisor.simulationReset()
        self.supervisor.simulationResetPhysics()
        return self.get_default_observation()

    def get_default_observation(self):
        """
        This method should be implemented to return a default/starting
        observation that is use-case dependant. It is used by the
        reset implementation above.

        :return: list-like, contains default agent observation
        """
        return NotImplementedError

    @abstractmethod
    def get_info(self):
        """
        This method can be implemented to return any diagnostic
        information on each step, e.g. for debugging purposes.
        """
        pass
