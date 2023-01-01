from controller import Keyboard

from deepbots.supervisor.controllers.deepbots_supervisor_env import \
    DeepbotsSupervisorEnv


class KeyboardPrinter(DeepbotsSupervisorEnv):
    def __init__(self, controller):
        self.controller = controller
        self.keyboard = Keyboard()
        self.keyboard.enable(self.controller.timestep)

    def step(self, action):
        observation, reward, is_done, info = self.controller.step(action)
        key = self.keyboard.getKey()
        # DEBUG CONTROLS
        if key == Keyboard.CONTROL + ord("A"):
            print()
            print("Actions: ", action)
        if key == Keyboard.CONTROL + ord("R"):
            print()
            print("Rewards: ", reward)
        if key == Keyboard.CONTROL + ord("Y"):
            print()
            print("Observations: ", self.controller.observation)

        return observation, reward, is_done, info

    def is_done(self):
        is_done = self.controller.is_done()
        if is_done:
            print("Done")
        return is_done

    def get_observations(self):
        return self.controller.get_observations()

    def get_reward(self, action):
        return self.controller.get_reward(action)

    def get_info(self):
        return self.controller.get_info()

    def reset(self):
        print("RESET")
        observations = self.controller.reset()
        return observations
