import random
from City import *
distances = []
cities_dict = {}


def initialize_population(cities, population_size):
    population = []
    start_city = cities[0]
    remaining_cities = cities[1:]
    for _ in range(population_size):
        random.shuffle(remaining_cities)
        path = [start_city] + remaining_cities + [start_city]
        population.append(path)
    return population


def get_fitness(path):
    global distances
    total_distance = 0
    for i in range(len(path) - 1):
        from_city = path[i]
        to_city = path[i + 1]
        total_distance += distances[from_city][to_city]
    return 1 / total_distance


def calculate_cumulative_sum(population):
    fitness_values = []
    for path in population:
        fitness_values.append(get_fitness(path))
    fitness_values = sorted(fitness_values, reverse=True)
    cumulative_fitness = [fitness_values[0]]
    for i in range(1, len(fitness_values)):
        cumulative_fitness.append(cumulative_fitness[i-1] + fitness_values[i])
    return cumulative_fitness


def roulette_wheel_selection(population):
    fitness_sum = sum(get_fitness(path) for path in population)
    random_number = random.uniform(0, fitness_sum)
    current_sum = 0
    for path in population:
        current_sum += get_fitness(path)
        if random_number <= current_sum:
            return path
    return population[-1]


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


def swap_mutation(individual):
    # Randomly select two distinct positions in the tour
    pos = random.choice(range(1, len(individual) - 2))
    # Swap the cities at the selected positions
    individual[pos], individual[pos+1] = individual[pos+1], individual[pos]
    return individual


def mutation(population, mutation_rate):
    mutated_population = []
    for unit in population:
        if random.random() < mutation_rate:
            mutated_population.append(swap_mutation(unit))
        else:
            mutated_population.append(unit)
    return mutated_population


def create_next_generation(parents, crossover_rate, population_size):
    next_generation = []
    while len(next_generation) < population_size:
        if random.random() < crossover_rate:
            parent1 = roulette_wheel_selection(parents)
            parent2 = roulette_wheel_selection(parents)
            child1, child2 = crossover(parent1, parent2)
            next_generation.append(child1)
            next_generation.append(child2)
        else:
            next_generation.append(roulette_wheel_selection(parents))
    next_generation = mutation(next_generation, 0.1)
    return next_generation


def launch_algorithm(cities):
    global distances
    global cities_dict
    cities_dict = cities
    cities_list = list(cities.keys())
    distances = all_distances(cities)
    initial_population = initialize_population(cities_list, 30)
    average_fitness_graph = [average_fitness(initial_population)]

    previous_population = initial_population
    next_population = None
    for i in range(0, 10000):
        next_population = create_next_generation(previous_population, 0.7, 50)
        if (i + 1) % 500 == 0:
            average_fitness_graph.append(average_fitness(next_population))
        previous_population = next_population

    best_fitness = 0
    best_unit = None
    for unit in next_population:
        current_fitness = get_fitness(unit)
        if best_fitness < current_fitness:
            best_unit = unit
            best_fitness = current_fitness
    return best_unit, best_fitness, average_fitness_graph


def average_fitness(population):
    fitness = 0
    for unit in population:
        fitness += get_fitness(unit)
    return fitness / len(population)
