from controller import Keyboard


class KeyboardPrinter:
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

    def isDone(self):
        isDone = self.controller.isDone()
        if isDone:
            print("Done")
        return isDone

    def reset(self):
        print("RESET")
        observations = self.controller.reset()
        return observations
