from deepbots.supervisor.controllers.supervisor_evolutionary import SupervisorEvolutionary

import pygad
import pygad.torchga as torchga
from pygad.torchga import TorchGA
import torch
import matplotlib.pyplot as plt
import wandb

class SupervisorMultiEvolutionary(SupervisorEvolutionary, pygad.GA):
    def __init__(self, num_robots, model, device=None):
        super().__init__(model, device)
        self.num_robots = num_robots

    def fitness_function(self, solution, solution_idx):
        """
        The default fitness function for the genetic algorithm. The fitness is defined as the total reward accumulated by 
        the agent over one episoder. This function can be overrided with a custom fitness function for the genetic algorithm 
        by re-defining in the inheriting class.

        :param solution: The solution vector of the model.
        :type solution: dict(torch.Tensor)
        :param solution_idx: The index of the solution vector in the population.
        :type solution_idx: int
        :return: The fitness value of the solution vector.
        :rtype: float
        """

        model_weights = torchga.model_weights_as_dict(model=self.model, weights_vector=solution)
        model_weights = {k: v.to(self.device) for k, v in model_weights.items()}
        self.model.load_state_dict(model_weights)

        observation = self.reset()
        total_reward = 0
        done = False
        no_steps = 0
        
        while not done:
            observation = torch.tensor(observation).unsqueeze(0).float().to(self.device)
            next_observation, reward, done, info = self.step(observation)
            self.episodeScore += reward
            observation = next_observation
            no_steps += 1

        return self.episodeScore

    def step(self, observation):
        """
        Take one step in the environment by using the model to predict the action to take.

        :param observation: The observation received from the environment.
        :type observation: torch.Tensor
        :return: The next observation, reward, done flag and info.
        :rtype: torch.Tensor, float, bool, dict
        """
        action = self.get_action(observation)
        next_observation, reward, done, info = super(SupervisorCSV, self).step(action)

        return next_observation, reward, done, info

    def cal_pop_fitness(self):
        if self.valid_parameters == False:
            raise ValueError("ERROR calling the cal_pop_fitness() method: \nPlease check the parameters passed while creating an instance of the GA class.\n")

        pop_fitness = []
        # Calculating the fitness value of each solution in the current population.
        for sol_idx, sol in enumerate(self.population):

            # Check if the parent's fitness value is already calculated. If so, use it instead of calling the fitness function.
            if not (self.last_generation_parents is None) and len(numpy.where(numpy.all(self.last_generation_parents == sol, axis=1))[0] > 0):
                # Index of the parent in the parents array (self.last_generation_parents). This is not its index within the population.
                parent_idx = numpy.where(numpy.all(self.last_generation_parents == sol, axis=1))[0][0]
                # Index of the parent in the population.
                parent_idx = self.last_generation_parents_indices[parent_idx]
                # Use the parent's index to return its pre-calculated fitness value.
                fitness = self.last_generation_fitness[parent_idx]
            else:
                fitness = self.fitness_func(sol, sol_idx)
            pop_fitness.append(fitness)

        pop_fitness = numpy.array(pop_fitness)

        return pop_fitness