from abc import ABC, abstractmethod

from controller import Supervisor


class SupervisorEnv(ABC):
    """
    This class represents the basic template which contains the necessary
    methods to train a reinforcement learning algorithm. The interface class
    follows the gym interface which is standardized in much many reinforcement
    learning algorithms. The OpenAI gym environment can be described by the
    following figure:

     +----------+             (action)            +---------------+
     |          |-------------------------------->|               |
     |   Agent  |                                 | SupervisorEnv |
     |          |<--------------------------------|               |
     +----------+      (observation, reward)      +---------------+

    """

    def __init__(self):
        self.supervisor = Supervisor()

    @abstractmethod
    def get_observations(self):
        """
        Return the observations of the robot. For example, metrics from
        sensors, camera image etc.



        :returns: An object of observations
        """
        pass

    @abstractmethod
    def step(self, action):
        """
        Each timestep, the agent chooses  an action, and the environment
        returns the observation, the reward and the state of the problem (done
        or not).

        observation: The observation from the environment
        reward: The amount of reward achieved by the previous action.
        is_done: If the problem is solved
        info: Diagnostic information mostly useful for debugging.

        :param action: The agent's action
        :return: tuple, (observation, reward, is_done, info)
        """
        pass

    @abstractmethod
    def get_reward(self, action):
        """
        :param action: The agent's action
        :return: the amount of reward achieved by the previous action.
        """
        pass

    @abstractmethod
    def is_done(self):
        """
        Used to inform the agent that the problem solved.

        :return: bool, True if the problem have been solved
        """
        pass

    def reset(self):
        """
        Used to reset the world to an initial state.

        Default implementation of reset method, using Webots-provided methods.

        *Note that this works properly only with Webots versions >R2020b and must be
        overridden with a custom reset method when using earlier versions. It is backwards compatible
        due to the fact that the new reset method gets overridden by whatever the user has previously
        implemented, so an old supervisor such as SupervisorCSV can be migrated easily to use this class.

        :return: default observation provided by get_default_observation() implementation
        """
        self.supervisor.simulationReset()
        self.supervisor.simulationResetPhysics()
        return self.get_default_observation()

    @abstractmethod
    def get_default_observation(self):
        """
        This method should be implemented to return a default/starting observation
        that is use-case dependant. It is mainly used by the reset implementation above.

        :return: list-like, contains default agent observation
        """
        pass

    @abstractmethod
    def get_info(self):
        """
         Diagnostic information mostly useful for debugging.
        """
        pass
