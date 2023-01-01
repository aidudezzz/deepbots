import numpy as np
from tensorboardX import SummaryWriter

from deepbots.supervisor.controllers.deepbots_supervisor_env import \
    DeepbotsSupervisorEnv


class TensorboardLogger(DeepbotsSupervisorEnv):
    def __init__(self,
                 controller,
                 log_dir="logs/results",
                 v_action=0,
                 v_observation=0,
                 v_reward=0,
                 windows=[10, 100, 200]):
        self.controller = controller

        self.step_cntr = 0
        self.step_global = 0
        self.step_reset = 0

        self.score = 0
        self.score_history = []

        self.v_action = v_action
        self.v_observation = v_observation
        self.v_reward = v_reward
        self.windows = windows

        self.file_writer = SummaryWriter(log_dir, flush_secs=30)

    def step(self, action):
        observation, reward, is_done, info = self.controller.step(action)

        if (self.v_action > 1):
            self.file_writer.add_histogram(
                "Actions/Per Global Step",
                action,
                global_step=self.step_global)

        if (self.v_observation > 1):
            self.file_writer.add_histogram(
                "Observations/Per Global Step",
                observation,
                global_step=self.step_global)

        if (self.v_reward > 1):
            self.file_writer.add_scalar("Rewards/Per Global Step", reward,
                                        self.step_global)

        if (is_done):
            self.file_writer.add_scalar(
                "Is Done/Per Reset step",
                self.step_cntr,
                global_step=self.step_reset)

        self.file_writer.flush()

        self.score += reward

        self.step_cntr += 1
        self.step_global += 1

        return observation, reward, is_done, info

    def is_done(self):
        is_done = self.controller.is_done()

        self.file_writer.flush()
        return is_done

    def get_observations(self):
        obs = self.controller.get_observations()

        return obs

    def get_reward(self, action):
        reward = self.controller.get_reward(action)
        return reward

    def get_info(self):
        info = self.controller.get_info()
        return info

    def reset(self):

        observations = self.controller.reset()
        self.score_history.append(self.score)

        if (self.v_observation > 0):
            self.file_writer.add_histogram(
                "Observations/Per Reset",
                observations,
                global_step=self.step_reset)

        if (self.v_reward > 0):
            self.file_writer.add_scalar(
                "Score/Per Reset", self.score, global_step=self.step_reset)

            for window in self.windows:
                if self.step_reset > window:
                    self.file_writer.add_scalar(
                        "Score/With Window {}".format(window),
                        np.average(self.score_history[-window:]),
                        global_step=self.step_reset - window)

        self.file_writer.flush()

        self.step_reset += 1
        self.step_cntr = 0
        self.score = 0

        return observations

    def flush(self):
        if self._file_writer is not None:
            self._file_writer.flush()

    def close(self):
        if self._file_writer is not None:
            self._file_writer.close()
