from _testcapi import INT_MAX

from Genetic import genetic, get_fitness
from TabuSearch import tabu_search
from SimulatedAnnealing import simulated_annealing
from City import generate_cities
import matplotlib.pyplot as plt
import numpy as np
import pickle
import time

global cities


def display_path(path, title):  # the graph function is generated with OpenAI ChatGPT
    global cities
    x_coords, y_coords = zip(*[cities[id] for id in path])

    # Plot the dots
    plt.scatter(x_coords, y_coords, label='Dots', color='blue')

    # Plot the path
    plt.plot(x_coords, y_coords, label='Path', linestyle='dashed', color='red')

    # Annotate dots with IDs
    for id in path:
        plt.annotate(str(id), cities[id], textcoords="offset points", xytext=(0, 5), ha='center')

    # Add labels and legend
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title(title)
    plt.legend()

    # Show the plot
    plt.show()


def display_average_fitness(average_fitness):  # the graph function is generated with OpenAI ChatGPT
    x_values = np.arange(0, len(average_fitness) * 500, 500)

    # Plotting the data
    plt.plot(x_values, average_fitness, marker='o', linestyle='-')

    # Adding labels and title
    plt.xlabel('X-axis (every 500 units)')
    plt.ylabel('Y-axis')
    plt.title('Average fitness progression')

    # Displaying the plot
    plt.show()


def manual_interaction():
    print("1. Genetic")
    print("2. Tabu Search")
    print("3. Simulated Annealing")
    algorithm = input("Choose the algorithm: ")
    if algorithm == "1":
        population_size = int(input("Enter population size: "))
        mutation_rate = float(input("Enter mutation rate: "))
        crossover_rate = float(input("Enter crossover rate: "))
        while True:
            selection_type = input("Enter selection type (tournament/roulette): ")
            if selection_type == "tournament" or selection_type == "roulette":
                break
            else:
                print("Wrong selection type")
        tournament_rate = 0.1
        if selection_type == "tournament":
            tournament_rate = float(input("Enter tournament rate: "))
        num_iterations = int(input("Enter number of iterations: "))
        start_time = time.time()
        solution, fitness, average_fitness_list = genetic(cities, population_size, mutation_rate, crossover_rate,
                                                          selection_type, num_iterations, tournament_rate)
        end_time = time.time()
        elapsed_time = end_time - start_time
        display_path(solution, f"Genetic solution with distance: {1/fitness}")
        display_average_fitness(average_fitness_list)
        print(f"Solution was found in {elapsed_time} seconds")
    elif algorithm == "2":
        num_iterations = int(input("Enter number of iterations: "))
        tabu_size = int(input("Enter size of tabu list: "))
        start_time = time.time()
        solution, distance = tabu_search(cities, num_iterations, tabu_size)
        end_time = time.time()
        display_path(solution, f"Tabu Search solution with distance of {distance}")
        print(f"The solution {solution} was found in {end_time-start_time} seconds")
    elif algorithm == "3":
        num_iterations = int(input("Enter number of iterations: "))
        temperature = int(input("Enter initial temperature: "))
        cooling = float(input("Enter cooling rate:"))
        start_time = time.time()
        solution, distance = simulated_annealing(cities, temperature, cooling, num_iterations)
        end_time = time.time()
        display_path(solution, f"Simulated Annealing solution with distance of {distance}")
        print(f"The solution {solution} was found in {end_time - start_time} seconds")
    else:
        print("Wrong choice")
def automatic_test():
    print("Tabu Search test:")
    num_iterations = max((len(cities) ** 2) * 10, 5000)
    print("Number of iterations is defined with formula max(num_of_cities^2 * 10, 5000): " + str(num_iterations))
    best_solution = None
    best_distance = INT_MAX
    elapsed_time_list = []
    tabu_table_size_list = []
    for j in range(10):
        start_time = time.time()
        path, distance = tabu_search(cities, num_iterations, num_iterations/1000*j*j)
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time_list.append(elapsed_time)
        tabu_table_size_list.append(num_iterations/1000*j*j)
        if distance < best_distance:
            best_solution = path
            best_distance = distance
    print(f"The best solution is {best_solution} with distance of {best_distance}")
    display_path(best_solution, f"Tabu Search best solution with {best_distance} distance")
    plt.plot(tabu_table_size_list, elapsed_time_list, marker='o', linestyle='-')
    plt.xlabel('Tabu Search table size')
    plt.ylabel('Elapsed time')
    plt.title('Elapsed time by size of tabu table size')
    plt.show()

    print("Simulated Annealing test: ")
    num_iterations = max((len(cities) ** 2) * 1000, 500000)
    temperature = len(cities) ** 2
    cooling_rate = 0.9999
    print("Number of iterations max(num_of_cities^2 * 1000, 500000): " + str(num_iterations))
    print(f"Default values: \n"
          f"Number of iterations = max(num_of_cities^2 * 1000, 500000): {num_iterations}"
          f"Temperature = num_of_cities^2 : {temperature}"
          f"Cooling rate: {cooling_rate}")
    best_temperature = None
    best_distance = INT_MAX

    elapsed_time_list = []
    distance_list = []
    initial_temperature_list = []
    for i in range(1, 10):
        start_time = time.time()
        current_temperature = temperature * i * i
        solution, distance = simulated_annealing(cities, current_temperature, cooling_rate, num_iterations)
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time_list.append(elapsed_time)
        distance_list.append(distance)
        initial_temperature_list.append(current_temperature)
        if distance < best_distance:
            best_temperature = current_temperature
            best_distance = distance
    plt.plot(initial_temperature_list, elapsed_time_list, marker='o', linestyle='-')
    plt.xlabel('Initial temperature')
    plt.ylabel('Elapsed time')
    plt.title('Elapsed time by initial temperature')
    plt.show()
    plt.plot(initial_temperature_list, distance_list, marker='o', linestyle='-')
    plt.xlabel('Initial temperature')
    plt.ylabel('Solution distance')
    plt.title('Solution distance by initial temperature')
    plt.show()
    print(f"Best initial temperature is: {best_temperature}")
    best_solution = None
    best_cooling = None
    best_distance = INT_MAX
    elapsed_time_list = []
    cooling_rate_list = []
    distance_list = []
    cooling_rate = 0.9
    for i in range(10):
        start_time = time.time()
        cooling_rate += 9 / (10 ** (i+2))
        print(cooling_rate)
        solution, distance = simulated_annealing(cities, best_temperature, cooling_rate, num_iterations)
        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time_list.append(elapsed_time)
        cooling_rate_list.append(cooling_rate)
        distance_list.append(distance)
        if distance < best_distance:
            best_solution = solution
            best_cooling = cooling_rate
            best_distance = distance
    print(f"Best solution found is {best_solution} with distance of {best_distance}")
    print(f"Parameters: \nInitial temperature: {best_temperature}\nCooling rate: {best_cooling}")
    display_path(best_solution, f"Simulated Annealing solution with distance {best_distance}")
    plt.plot(cooling_rate_list, elapsed_time_list, marker='o', linestyle='-')
    plt.xlabel('Initial temperature')
    plt.ylabel('Solution distance')
    plt.title('Solution distance by initial temperature')
    plt.show()
    plt.plot(cooling_rate_list, distance_list, marker='o', linestyle='-')
    plt.xlabel('Initial temperature')
    plt.ylabel('Solution distance')
    plt.title('Solution distance by initial temperature')
    plt.show()


if __name__ == '__main__':
    global cities
    while True:
        print("1. Example")
        print("2. Random generating")
        print("3. Manual input")
        problem_input = input("Choose the problem to solve: ")
        if problem_input == "1":
            with open("example_cities.pkl", 'rb') as file:
                cities = pickle.load(file)
            break
        elif problem_input == "2":
            number_of_cities = input("Enter number of cities to generate: ")
            width, height = input("Enter width and height of the map: ")
            cities = generate_cities(int(number_of_cities), int(width), int(height))
            break
        elif problem_input == "3":
            print("Enter -1 if the list is ready")
            cities = {}
            id = 0
            while True:
                x, y = input(f"Enter x, y coordinates for {id + 1}th city: ")
                if x == "-1" or y == "-1":
                    break
                cities[id] = int(x), int(y)
            break
        else:
            print("Wrong input")
    while True:
        print("1. Automatic test")
        print("2. Manual selection")
        print("3. Done")
        interaction = input("Choose your interaction type: ")
        if interaction == "1":
            automatic_test()
        elif interaction == "2":
            manual_interaction()
        elif interaction == "3":
            break
        else:
            print("Wrong interaction type")
