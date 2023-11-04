import random


class Unit:
    def __init__(self, path, fitness):
        self.path = path
        self.fitness = fitness

    def __str__(self):
        result = "path: "
        for i in range(len(self.path)):
            result += str(self.path[i].city_id) + " "
        result += f"Distance: {1 / self.fitness}"
        return result


def initialize_population(cities, population_size, distances):
    population = []
    start_city = cities[0]
    remaining_cities = cities[1:]
    for _ in range(population_size):
        random.shuffle(remaining_cities)
        path = [start_city] + remaining_cities + [start_city]
        fitness = get_fitness(path, distances)
        unit = Unit(path, fitness)
        population.append(unit)
    return population


def get_fitness(unit, distances):
    total_distance = 0
    for i in range(len(unit) - 1):
        from_city = unit[i]
        to_city = unit[i + 1]
        total_distance += distances[from_city.city_id][to_city.city_id]
    return 1 / total_distance


def calculate_cumulative_sum(population):
    fitness_values = []
    for unit in population:
        fitness_values.append(unit.fitness)
    fitness_values = sorted(fitness_values, reverse=True)
    cumulative_fitness = [fitness_values[0]]
    for i in range(1, len(fitness_values)):
        cumulative_fitness.append(cumulative_fitness[i-1] + fitness_values[i])
    return cumulative_fitness


def roulette_wheel_selection(population):
    cumulative_fitness = calculate_cumulative_sum(population)
    fitness_sum = 0
    for unit in population:
        fitness_sum += unit.fitness
    random_number = random.uniform(0, fitness_sum)
    for i in range(len(population)):
        if random_number <= cumulative_fitness[i]:
            return population[i]
    return population[-1]


