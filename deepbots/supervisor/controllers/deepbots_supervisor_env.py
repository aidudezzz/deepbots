import gym
from controller import Supervisor


class DeepbotsSupervisorEnv(Supervisor, gym.Env):
    """
    This class is the highest class in deepbots class hierarchy, inheriting
    both the Webots Supervisor controller and the basic gym.Env.

    Refer to gym.Env documentation on how to implement a custom gym.Env
    for additional functionality.

    This class contains abstract methods that guide the development process
    for users that want to implement a simple environment.

    This class is not intended for user usage, but to provide a common
    interface for all provided supervisor classes and make them
    compatible with reinforcement learning agents that work with
    the gym interface. Moreover, a problem-agnostic reset method is
    provided. Please use any of the children supervisor classes to be
    inherited by your own class, such as the RobotSupervisorEnv class.
    Nevertheless, advanced users can inherit this class to create
    their own supervisor classes if they wish.
    """

    def step(self, action):
        """
        On each timestep, the agent chooses an action for the previous
        observation, *state_t*, and the environment returns the next
        observation, *state_t+1*, the reward and whether the episode
        is done or not.

        Each of the values returned is produced by implementations of
        other abstract methods defined below.

        observation: The next observation from the environment
        reward: The amount of reward awarded on this step
        is_done: Whether the episode is done
        info: Diagnostic information mostly useful for debugging

        :param action: The agent's action
        :return: tuple, (observation, reward, is_done, info)
        """
        raise NotImplementedError

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
        self.simulationReset()
        self.simulationResetPhysics()
        super(Supervisor, self).step(int(self.getBasicTimeStep()))
        return self.get_default_observation()

    def get_default_observation(self):
        """
        This method should be implemented to return a default/starting
        observation that is use-case dependant. It is used by the
        reset implementation above.

        :return: list-like, contains default agent observation
        """
        raise NotImplementedError

    def get_observations(self):
        """
        Return the observations of the robot. For example, metrics from
        sensors, a camera image, etc.

        This method is use-case specific and needs to be implemented
        by the user.

        :returns: An object of observations
        """
        raise NotImplementedError

    def get_reward(self, action):
        """
        Calculates and returns the reward for this step.

        This method is use-case specific and needs to be implemented
        by the user.

        :param action: The agent's action
        :return: The amount of reward awarded on this step
        """
        raise NotImplementedError

    def is_done(self):
        """
        Used to inform the agent that the problem is solved.

        This method is use-case specific and needs to be implemented
        by the user.

        :return: bool, True if the episode is done
        """
        raise NotImplementedError

    def get_info(self):
        """
        This method can be implemented to return any diagnostic
        information on each step, e.g. for debugging purposes.
        """
        raise NotImplementedError
