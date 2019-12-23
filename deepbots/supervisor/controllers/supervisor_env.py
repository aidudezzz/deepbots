from abc import ABC, abstractmethod


class SupervisorEnv(ABC):
    '''
    This class represent the basic template which contains those necessary
    methods to train a reinforcement learning algorithm. The interface class
    follows the gym interface which is standardized in much many reinforcement
    learning algorithm. The OpenAI gym environment can be described by the
    following figure:

     +----------+             (action)            +---------------+
     |          |-------------------------------->|               |
     |   Agent  |                                 | SupervisorEnv |
     |          |<--------------------------------|               |
     +----------+      (observation, reward)      +---------------+

    '''
    @abstractmethod
    def get_observations(self):
        '''
        Return the observations of the robot. For example, metrics from
        sensors, camera image etc.

        Returns
        -------
        An object of observations
        '''
        pass

    @abstractmethod
    def step(self, action):
        '''
        Each timestep, the agent choose  an action, and the environment returns
        the observation, the reward and the state of the problem (done or not).

        Parameters
        ----------
        action: The agent's action

        Returns
        -------
        observation: The observation from the environment
        reward: The amount of reward achieved by the previous action.
        is_done: If the problem is solved
        info: Diagnostic information mostly useful for debugging.
        '''
        pass

    @abstractmethod
    def get_reward(self, action):
        '''
        Parameters
        ----------
        action: The agent's action

        Returns
        -------
        The amount of reward achieved by the previous action.
        '''
        pass

    @abstractmethod
    def is_done(self):
        '''
        Used to inform the agent that the problem solved.

        Returns
        -------
        bool
           True if the problem have been solved
        '''
        pass

    @abstractmethod
    def reset(self):
        '''
        Used to reset the world to an initial state.

        Returns
        -------
        observation: The observation from the environment
        reward: The amount of reward achieved by the previous action.
        is_done: If the problem is solved
        info: Diagnostic information mostly useful for debugging.
        '''
        pass

    @abstractmethod
    def get_info(self):
        '''
         Diagnostic information mostly useful for debugging.
        '''
        pass
