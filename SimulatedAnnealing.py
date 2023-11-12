from City import all_distances
import random
import math
distances = []


def calculate_total_distance(order):
    global distances
    total_distance = 0
    num_cities = len(order)

    for i in range(num_cities - 1):  # calculate the length of the path using distance matrix
        total_distance += distances[order[i]][order[i + 1]]

    return total_distance


def generate_initial_path(cities):
    start_city = cities[0]
    remaining_cities = cities[1:]
    random.shuffle(remaining_cities)    # all cities except the first one are shuffled
    result = [start_city] + remaining_cities + [start_city]     # the first city is the start and the end of the path
    return result


def generate_neighbour(path):
    new_path = path.copy()
    i, j = random.sample(range(1, len(path) - 1), 2)
    new_path[i], new_path[j] = new_path[j], new_path[i]     # generate a neighbor by swapping two random cities
    return new_path


def simulated_annealing(cities, initial_temperature, cooling_rate, num_iterations):
    cities_list = list(cities.keys())
    global distances
    distances = all_distances(cities)
    current_path = generate_initial_path(cities_list)
    current_distance = calculate_total_distance(current_path)

    best_path = current_path
    best_distance = current_distance

    temperature = initial_temperature

    for iteration in range(num_iterations):
        neighbour_path = generate_neighbour(current_path)
        neighbour_distance = calculate_total_distance(neighbour_path)

        # if the neighbor is better, accept it
        if (neighbour_distance < current_distance or
                random.random() < math.exp((current_distance - neighbour_distance) / temperature)):
            current_path = neighbour_path
            current_distance = neighbour_distance

        # update the best solution if needed
        if current_distance < best_distance:
            best_path = current_path
            best_distance = current_distance

        # cool down the temperature
        temperature *= cooling_rate

    return best_path, best_distance
