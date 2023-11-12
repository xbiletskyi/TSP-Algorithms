import random
from City import *
distances = []
cities_dict = {}


def initialize_population(cities, population_size):
    population = []
    start_city = cities[0]  # the first and the last point of the path
    remaining_cities = cities[1:]
    for _ in range(population_size):
        random.shuffle(remaining_cities)
        path = [start_city] + remaining_cities + [start_city]   # the path goes through every city
        population.append(path)
    return population


def get_fitness(path):
    global distances
    total_distance = 0
    for i in range(len(path) - 1):
        from_city = path[i]
        to_city = path[i + 1]
        total_distance += distances[from_city][to_city]
    return 1 / total_distance   # fitness is derived from the total length of the path


def roulette_wheel_selection(population):
    fitness_sum = sum(get_fitness(path) for path in population)  # the roulette wheel itself
    random_number = random.uniform(0, fitness_sum)      # where the ball falls
    current_sum = 0
    for path in population:
        current_sum += get_fitness(path)        # fitness is the size of slot for each individual
        if random_number <= current_sum:        # the more this size, the more chance for being selected
            return path
    return population[-1]


def tournament_selection(population, tournament_rate):
    tournament_size = int(len(population) * tournament_rate)
    tournament_candidates = random.sample(range(len(population)), tournament_size)  # random sample of the population
    winner = max(tournament_candidates, key=lambda i: get_fitness(population[i]))   # select the one with the most fitness value
    return population[winner]


def crossover(parent1, parent2):
    # choose two distinct random points for crossover
    point1, point2 = random.sample(range(1, len(parent1) - 1), 2)
    point1, point2 = min(point1, point2), max(point1, point2)  # ensure point1 < point2
    # initialize children with the same starting and ending city
    child1 = [parent1[0]] + [-1] * (len(parent1) - 2) + [parent1[0]]
    child2 = [parent2[0]] + [-1] * (len(parent2) - 2) + [parent2[0]]
    # copy the segment between the two points from parents to children
    child1[point1:point2] = parent1[point1:point2]
    child2[point1:point2] = parent2[point1:point2]
    # fill in the remaining cities in children in the order they appear in the other parent
    for i in range(1, len(parent1) - 1):
        if parent2[i] not in child1:
            for j in range(1, len(parent1) - 1):
                if child1[j] == -1:
                    child1[j] = parent2[i]
                    break
    for i in range(1, len(parent1) - 1):
        if parent1[i] not in child2:
            for j in range(1, len(parent1) - 1):
                if child2[j] == -1:
                    child2[j] = parent1[i]
                    break
    return child1, child2


def swap_mutation(path):
    # randomly select two distinct positions in the tour
    pos = random.choice(range(1, len(path) - 2))
    # swap the cities at the selected positions
    path[pos], path[pos + 1] = path[pos + 1], path[pos]
    return path


def mutation(population, mutation_rate):
    mutated_population = []
    for unit in population:
        if random.random() < mutation_rate:     # decide whether this particular individual mutates
            mutated_population.append(swap_mutation(unit))
        else:
            mutated_population.append(unit)
    return mutated_population


def generate_new_population(parents, population_size, selection_type="tournament", crossover_rate=0.5,
                            mutation_rate=0.05, tournament_rate=0.1):
    next_generation = []
    while len(next_generation) < population_size:
        if random.random() < crossover_rate:    # decide whether to create new individuals
            if selection_type == "roulette":       # selection with different approaches
                parent1 = roulette_wheel_selection(parents)
                parent2 = roulette_wheel_selection(parents)
            elif selection_type == "tournament":
                parent1 = tournament_selection(parents, tournament_rate)
                parent2 = tournament_selection(parents, tournament_rate)
            else:
                return
            child1, child2 = crossover(parent1, parent2)
            next_generation.append(child1)
            next_generation.append(child2)
        else:
            if selection_type == "roulette":       # append existing individuals to new generation
                next_generation.append(roulette_wheel_selection(parents))
            elif selection_type == "tournament":
                next_generation.append(tournament_selection(parents, tournament_rate))
            else:
                return
    next_generation = mutation(next_generation, mutation_rate)  # mutate the population
    return next_generation


def genetic(cities, population_size, mutation_rate, crossover_rate, selection_type, num_iterations,
            tournament_rate=0.1):
    global distances
    global cities_dict
    cities_dict = cities
    cities_list = list(cities.keys())
    distances = all_distances(cities)
    initial_population = initialize_population(cities_list, population_size)
    average_fitness_graph = [average_fitness(initial_population)]   # a list for statistics

    best_fitness = 0
    best_unit = None

    previous_population = initial_population
    for i in range(num_iterations):
        next_population = generate_new_population(previous_population, population_size, selection_type,
                                                  crossover_rate, mutation_rate, tournament_rate)
        if (i + 1) % 500 == 0:  # adds the average fitness every 500 generations
            average_fitness_graph.append(average_fitness(next_population))
        for path in next_population:    # update the best individual ever met
            current_fitness = get_fitness(path)
            if best_fitness < current_fitness:
                best_unit = path
                best_fitness = current_fitness

        previous_population = next_population

    return best_unit, best_fitness, average_fitness_graph


def average_fitness(population):
    fitness = 0
    for path in population:
        fitness += get_fitness(path)
    return fitness / len(population)
