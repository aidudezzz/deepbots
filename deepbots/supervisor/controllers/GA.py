import pygad

class GA(pygad.GA):
    def __init__(self, **kwargs):
        super(GA, self).__init__(**kwargs)

    def cal_pop_fitness(self):

        """
        Calculating the fitness values of all solutions in the current population. 
        It returns:
            -fitness: An array of the calculated fitness values.
        """

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
    
    def run(self):

        """
        Runs the genetic algorithm. This is the main method in which the genetic algorithm is evolved through a number of generations.
        """

        if self.valid_parameters == False:
            raise ValueError("Error calling the run() method: \nThe run() method cannot be executed with invalid parameters. Please check the parameters passed while creating an instance of the GA class.\n")

        # Reset the variables that store the solutions and their fitness after each generation. If not reset, then for each call to the run() method the new solutions and their fitness values will be appended to the old variables and their length double. Some errors arise if not reset.
        # If, in the future, new variables are created that get appended after each generation, please consider resetting them here.
        self.best_solutions = [] # Holds the best solution in each generation.
        self.best_solutions_fitness = [] # A list holding the fitness value of the best solution for each generation.
        self.solutions = [] # Holds the solutions in each generation.
        self.solutions_fitness = [] # Holds the fitness of the solutions in each generation.

        if not (self.on_start is None):
            self.on_start(self)

        stop_run = False

        # Measuring the fitness of each chromosome in the population. Save the fitness in the last_generation_fitness attribute.
        self.last_generation_fitness = self.cal_pop_fitness()

        best_solution, best_solution_fitness, best_match_idx = self.best_solution(pop_fitness=self.last_generation_fitness)

        # Appending the best solution in the initial population to the best_solutions list.
        if self.save_best_solutions:
            self.best_solutions.append(best_solution)

        # Appending the solutions in the initial population to the solutions list.
        if self.save_solutions:
            self.solutions.extend(self.population.copy())

        for generation in range(self.num_generations):
            if not (self.on_fitness is None):
                self.on_fitness(self, self.last_generation_fitness)

            # Appending the fitness value of the best solution in the current generation to the best_solutions_fitness attribute.
            self.best_solutions_fitness.append(best_solution_fitness)
            
            if self.save_solutions:
                self.solutions_fitness.extend(self.last_generation_fitness)

            # Selecting the best parents in the population for mating.
            if callable(self.parent_selection_type):
                self.last_generation_parents, self.last_generation_parents_indices = self.select_parents(self.last_generation_fitness, self.num_parents_mating, self)
            else:
                self.last_generation_parents, self.last_generation_parents_indices = self.select_parents(self.last_generation_fitness, num_parents=self.num_parents_mating)
            if not (self.on_parents is None):
                self.on_parents(self, self.last_generation_parents)

            # If self.crossover_type=None, then no crossover is applied and thus no offspring will be created in the next generations. The next generation will use the solutions in the current population.
            if self.crossover_type is None:
                if self.num_offspring <= self.keep_parents:
                    self.last_generation_offspring_crossover = self.last_generation_parents[0:self.num_offspring]
                else:
                    self.last_generation_offspring_crossover = numpy.concatenate((self.last_generation_parents, self.population[0:(self.num_offspring - self.last_generation_parents.shape[0])]))
            else:
                # Generating offspring using crossover.
                if callable(self.crossover_type):
                    self.last_generation_offspring_crossover = self.crossover(self.last_generation_parents,
                                                                              (self.num_offspring, self.num_genes),
                                                                              self)
                else:
                    self.last_generation_offspring_crossover = self.crossover(self.last_generation_parents,
                                                                              offspring_size=(self.num_offspring, self.num_genes))
                if not (self.on_crossover is None):
                    self.on_crossover(self, self.last_generation_offspring_crossover)

            # If self.mutation_type=None, then no mutation is applied and thus no changes are applied to the offspring created using the crossover operation. The offspring will be used unchanged in the next generation.
            if self.mutation_type is None:
                self.last_generation_offspring_mutation = self.last_generation_offspring_crossover
            else:
                # Adding some variations to the offspring using mutation.
                if callable(self.mutation_type):
                    self.last_generation_offspring_mutation = self.mutation(self.last_generation_offspring_crossover, self)
                else:
                    self.last_generation_offspring_mutation = self.mutation(self.last_generation_offspring_crossover)
                if not (self.on_mutation is None):
                    self.on_mutation(self, self.last_generation_offspring_mutation)

            if (self.keep_parents == 0):
                self.population = self.last_generation_offspring_mutation
            elif (self.keep_parents == -1):
                # Creating the new population based on the parents and offspring.
                self.population[0:self.last_generation_parents.shape[0], :] = self.last_generation_parents
                self.population[self.last_generation_parents.shape[0]:, :] = self.last_generation_offspring_mutation
            elif (self.keep_parents > 0):
                parents_to_keep, _ = self.steady_state_selection(self.last_generation_fitness, num_parents=self.keep_parents)
                self.population[0:parents_to_keep.shape[0], :] = parents_to_keep
                self.population[parents_to_keep.shape[0]:, :] = self.last_generation_offspring_mutation

            self.generations_completed = generation + 1 # The generations_completed attribute holds the number of the last completed generation.

            # Measuring the fitness of each chromosome in the population. Save the fitness in the last_generation_fitness attribute.
            self.last_generation_fitness = self.cal_pop_fitness()

            best_solution, best_solution_fitness, best_match_idx = self.best_solution(pop_fitness=self.last_generation_fitness)

            # Appending the best solution in the current generation to the best_solutions list.
            if self.save_best_solutions:
                self.best_solutions.append(best_solution)

            # Appending the solutions in the current generation to the solutions list.
            if self.save_solutions:
                self.solutions.extend(self.population.copy())

            # If the callback_generation attribute is not None, then cal the callback function after the generation.
            if not (self.on_generation is None):
                r = self.on_generation(self)
                if type(r) is str and r.lower() == "stop":
                    # Before aborting the loop, save the fitness value of the best solution.
                    _, best_solution_fitness, _ = self.best_solution(self.last_generation_fitness)
                    self.best_solutions_fitness.append(best_solution_fitness)
                    break

            if not self.stop_criteria is None:
                for criterion in self.stop_criteria:
                    if criterion[0] == "reach":
                        if max(self.last_generation_fitness) >= criterion[1]:
                            stop_run = True
                            break
                    elif criterion[0] == "saturate":
                        criterion[1] = int(criterion[1])
                        if (self.generations_completed >= criterion[1]):
                            if (self.best_solutions_fitness[self.generations_completed - criterion[1]] - self.best_solutions_fitness[self.generations_completed - 1]) == 0:
                                stop_run = True
                                break

            if stop_run:
                break

            time.sleep(self.delay_after_gen)

        # Save the fitness of the last generation.
        if self.save_solutions:
            self.solutions_fitness.extend(self.last_generation_fitness)

        # Save the fitness value of the best solution.
        _, best_solution_fitness, _ = self.best_solution(pop_fitness=self.last_generation_fitness)
        self.best_solutions_fitness.append(best_solution_fitness)

        self.best_solution_generation = numpy.where(numpy.array(self.best_solutions_fitness) == numpy.max(numpy.array(self.best_solutions_fitness)))[0][0]
        # After the run() method completes, the run_completed flag is changed from False to True.
        self.run_completed = True # Set to True only after the run() method completes gracefully.

        if not (self.on_stop is None):
            self.on_stop(self, self.last_generation_fitness)

        # Converting the 'best_solutions' list into a NumPy array.
        self.best_solutions = numpy.array(self.best_solutions)

        # Converting the 'solutions' list into a NumPy array.
        self.solutions = numpy.array(self.solutions)
