from abc import abstractmethod

from controller import Supervisor

from deepbots.supervisor.controllers.supervisor_env import SupervisorEnv


class RobotSupervisor(SupervisorEnv):
    """
        step(action) (+ run or similar)
        create_message() analogous method (to be named) - This will be inside the get_observations implementation anyway
        use_message_data() analogous method (to be named) - Renamed to apply_action(action)
        reset(), this one will use the new reset procedure of Webots R2020 providing
            generic reset functionality for the user
    """
    def __init__(self, time_step=None):
        super(RobotSupervisor, self).__init__()

        self.robotSupervisor = Supervisor()

        if time_step is None:
            self.timestep = int(self.robotSupervisor.getBasicTimeStep())
        else:
            self.timestep = time_step

    def get_timestep(self):
        return self.timestep

    def step(self, action):
        self.robotSupervisor.step(self.timestep)

        self.apply_action(action)
        return (
            self.get_observations(),
            self.get_reward(action),
            self.is_done(),
            self.get_info(),
        )

    def reset(self):
        self.robotSupervisor.simulationReset()
        self.robotSupervisor.simulationResetPhysics()
        return self.get_default_observation()

    @abstractmethod
    def get_default_observation(self):
        """
        This method should return a default observation for e.g.
        after resetting.
        :return: list, contains default agent observation
        """
        pass

    @abstractmethod
    def apply_action(self, action):
        """
        This method should be implemented to apply whatever actions the
        action argument contains.
        :param action: list, containing action data
        """
        pass
