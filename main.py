from City import *
from Algorithm import *

if __name__ == '__main__':
    cities_list = generate_cities(10, 200, 200)
    distances = all_distances(cities_list)
    population = initialize_population(cities_list, 10, distances)
    cumulative_sum = calculate_cumulative_sum(population)
    for unit in population:
        print(str(1 / unit.fitness))
    print()
    for i in cumulative_sum:
        print((1 / i))

