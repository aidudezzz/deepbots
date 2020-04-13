from controller import Keyboard

from deepbots.supervisor.controllers.supervisor_env import SupervisorEnv


class KeyboardPrinter(SupervisorEnv):
    def __init__(self, controller):
        self.controller = controller
        self.keyboard = Keyboard()
        self.keyboard.enable(self.controller.get_timestep())

    def step(self, action):
        observation, reward, isDone, info = self.controller.step(action)
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

        return observation, reward, isDone, info

    def is_done(self):
        isDone = self.controller.is_done()
        if isDone:
            print("Done")
        return isDone

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
