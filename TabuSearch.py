import random
from City import all_distances

distances = []


def calculate_total_distance(path):
    global distances
    total_distance = 0
    num_cities = len(path)
    for i in range(num_cities - 1):  # calculate the length of the path using distance matrix
        total_distance += distances[path[i]][path[i + 1]]
    return total_distance


def generate_initial_path(cities):
    start_city = cities[0]
    remaining_cities = cities[1:]
    random.shuffle(remaining_cities)    # all cities except the first one are shuffled
    result = [start_city] + remaining_cities + [start_city]  # the first city is the start and the end of the path
    return result


def generate_neighbour(path):
    neighbour = path.copy()
    i, j = random.sample(range(1, len(path) - 1), 2)
    neighbour[i], neighbour[j] = neighbour[j], neighbour[i]     # generate a neighbor by swapping two random cities
    return neighbour


def tabu_search(cities, max_iterations, tabu_list_size):
    global distances
    distances = all_distances(cities)
    cities_list = list(cities.keys())
    num_cities = len(cities_list)
    current_path = generate_initial_path(cities_list)
    best_path = current_path.copy()
    tabu_list = []

    for iteration in range(max_iterations):
        neighbours = [generate_neighbour(current_path) for _ in range(num_cities * 2)]

        # evaluate neighbors and choose the best non-tabu move
        best_neighbour = min(neighbours, key=lambda x: calculate_total_distance(x))
        while best_neighbour in tabu_list:
            neighbours.remove(best_neighbour)
            best_neighbour = min(neighbours, key=lambda x: calculate_total_distance(x))

        # update current solution and tabu list
        current_path = best_neighbour
        tabu_list.append(best_neighbour)
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)  # Remove the oldest move from the tabu list

        # update the best solution if a better one is found
        if calculate_total_distance(current_path) < calculate_total_distance(best_path):
            best_path = current_path

    return best_path, calculate_total_distance(best_path)
