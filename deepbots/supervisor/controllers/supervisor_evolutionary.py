from deepbots.deepbots.supervisor.controllers.supervisor_emitter_receiver import SupervisorCSV

import pygad.GA as GA
import pygad.torchga as torchga
from pygad.torchga import TorchGA
import torch

class SupervisorEvolutionary(SupervisorCSV):
    '''
    TODO:
        - Add gpu compatibility
        - Add more logging and Tensorboard / wandb integration
        - Add docstrings
        - Add more kwargs for PyGAD GA
        - Add exceptions
        - Change comm scheme and add support for multiple robots
    '''
        
    def __init__(self, model):
        super(SupervisorEvolutionary, self).__init__()
        self.model = model

    def fitness_function(self, solution, solution_idx):
        # ToDo : Add gpu compatibility
        model_weights = torchga.model_weights_as_dict(model=self.model, weights_vector=solution)
        self.model.load_state_dict(model_weights)

        observation = self.reset()
        observation = torch.tensor(observation).unsqueeze(0)
        total_reward = 0
        done = False
        no_steps = 0
        
        while not done and no_steps < 1000:
            next_observation, reward, done, info = self.step(observation)
            total_reward += reward
            observation = next_observation

        return total_reward

    def step(self, observation):
        self.get_action(observation)
        next_observation, reward, done, info = super(SupervisorCSV, self).step(action)

        return next_observation, reward, done, info

    def get_action(self, observation):
        raise NotImplementedError

    def callback_generation(self, ga_solver):
        # ToDo : Add more logging and Tensorboard / Wandb integration
        print(f"Generation: {ga_solver.generations_completed} | Fitness: {ga_solver.best_solver()[1]}")

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
    ):

        initial_population = TorchGA(model=self.model, num_solutions=num_solutions).population_weights
    
        self.ga_solver = GA(
                    num_generations=num_generations,
                    num_parents_mating=num_parents_mating,
                    initial_population=initial_population,
                    fitness_func=self.fitness_function,
                    parent_selection_type=parent_selection_type,
                    crossover_type=crossover_type,
                    mutation_type=mutation_type,
                    mutation_percent_genes=mutation_percent_genes,
                    keep_parent=keep_parents,
                    on_generation=self.callback_generation
                )

        self.ga_solver.run()
        solution, solution_fitness, solution_idx = self.ga_solver.best_solution()
        trained_model_weights = torchga.model_weights_as_dict(model=self.model, weights_vector=solution)
        self.model.load_state_dict(trained_model_weights)
        print(f"Fitness value of best solution = {solution_fitness}")

        return self.model, solution_fitness, solution_idx

    def save_model(self, path):
        torch.save(self.model.state_dict(), path)

    def plot_fitness(self):
        self.ga_solver.plot_fitness(title="Fitness vs Generation", linewidth=3)




