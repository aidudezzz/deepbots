from deepbots.supervisor.controllers.supervisor_emitter_receiver import SupervisorCSV

import pygad
import pygad.torchga as torchga
from pygad.torchga import TorchGA
import torch
from functools import partial
import matplotlib.pyplot as plt

class SupervisorEvolutionary(SupervisorCSV):
    '''
    TODO:
        - Add more logging and Tensorboard / wandb integration
        - Change comm scheme and add support for multiple robots
    '''
        
    def __init__(self, model, device):
        """
        The base class for implementing genetic algorithms using deepbots.

        :param model: The model to be trained and used in the genetic algorithm.
        :type model: torch.nn.Module
        :param device: The device to be used for training the model.
        :type device: torch.device
        """
        super(SupervisorEvolutionary, self).__init__()
        self.fitness = []
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = model.to(device)
        self.device = device
        #self.count = 0

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
        #print("Reset")
        #print(self.count)
        #self.count += 1
        model_weights = torchga.model_weights_as_dict(model=self.model, weights_vector=solution)
        model_weights = {k: v.to(self.device) for k, v in model_weights.items()}
        self.model.load_state_dict(model_weights)

        observation = self.reset()
        total_reward = 0
        done = False
        no_steps = 0
        
        while not done and no_steps < 1000:
            observation = torch.tensor(observation).unsqueeze(0).float().to(self.device)
            next_observation, reward, done, info = self.step(observation)
            total_reward += reward
            observation = next_observation

        return total_reward

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

    def get_action(self, observation):
        """
        Get the action to be taken by the agent.

        :param observation: The observation received from the environment.
        :type observation: torch.Tensor
        """
        raise NotImplementedError

    def callback_generation(self, ga_solver):
        """
        Callback function for the genetic algorithm solver. This function is called after each generation and prints fitness 
        of the best solution in the generation.

        :param ga_solver: The genetic algorithm solver object.
        :type ga_solver: pygad.GA
        """
        # TODO : Add more logging and Tensorboard / Wandb integration
        print(f"Generation: {ga_solver.generations_completed} | Fitness: {ga_solver.best_solution()[1]}")
        self.fitness.append(ga_solver.best_solution()[1])

    def train(
        self,
        num_generations=75, 
        num_parents_mating=5,
        num_solutions=10,
        parent_selection_type="sss", 
        crossover_type="single_point",
        mutation_type="random",
        mutation_percent_genes=10, 
        keep_parents=-1, 
        **kwargs,
    ):
        """
        Method to train the model using the genetic algorithm.

        :param num_generations: The number of generations to be trained for.
        :type num_generations: int
        :param num_parents_mating: The number of parents to be selected for mating.
        :type num_parents_mating: int
        :param num_solutions: The number of solutions to be selected for mating.
        :type num_solutions: int
        :param parent_selection_type: The type of parent selection to be used.
        :type parent_selection_type: str
        :param crossover_type: The type of crossover to be used.
        :type crossover_type: str
        :param mutation_type: The type of mutation to be used.
        :type mutation_type: str
        :param mutation_percent_genes: The percentage of genes to be mutated.
        :type mutation_percent_genes: int
        :param keep_parents: The number of parents to keep in the population.
        :type keep_parents: int
        :param kwargs: Other keyword arguments for the genetic algorithm solver.
        :type kwargs: dict

        :return: The model loaded with the best solution, the fitness of the best solution and its index, the history of 
                 the fitness.
        :rtype: torch.nn.Module, float, int, list
        """
        initial_population = TorchGA(model=self.model, num_solutions=num_solutions).population_weights
        #print(f"Initial population len: {initial_population[0].shape}")
        fitness_func = lambda solution, solution_idx: self.fitness_function(solution=solution, solution_idx=solution_idx)
        callback = lambda ga_solver: self.callback_generation(ga_solver=ga_solver)
        #partial(fitness_func, model=self.model)
    
        self.ga_solver = pygad.GA(
                    num_generations=num_generations,
                    num_parents_mating=num_parents_mating,
                    initial_population=initial_population,
                    fitness_func=fitness_func,
                    parent_selection_type=parent_selection_type,
                    crossover_type=crossover_type,
                    mutation_type=mutation_type,
                    mutation_percent_genes=mutation_percent_genes,
                    keep_parents=keep_parents,
                    on_generation=callback,
                    **kwargs,
                )

        self.ga_solver.run()
        solution, solution_fitness, solution_idx = self.ga_solver.best_solution()
        trained_model_weights = torchga.model_weights_as_dict(model=self.model, weights_vector=solution)
        trained_model_weights = {k: v.to(self.device) for k, v in trained_model_weights.items()}
        self.model.load_state_dict(trained_model_weights)
        print(f"Fitness value of best solution = {solution_fitness}")
        self.plot_fitness()

        return self.model, solution_fitness, solution_idx, self.fitness

    def save_model(self, path):
        """
        Function to save the model.

        :param path: The path to save the model.
        :type path: str
        """
        torch.save(self.model.state_dict(), path)

    def plot_fitness(self):
        """
        Function to plot the fitness history.
        """
        plt.plot(self.fitness)
        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Fitness vs Generation Plot")
        plt.show()




