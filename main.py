from Algorithm import *
import matplotlib.pyplot as plt
import numpy as np
import pickle


def display_path(path):
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
    title = "Fitness: " + str(get_fitness(path))
    plt.title(title)
    plt.legend()

    # Show the plot
    plt.show()

def display_average_fitness(average_fitness):
    x_values = np.arange(0, len(average_fitness) * 500, 500)

    # Plotting the data
    plt.plot(x_values, average_fitness, marker='o', linestyle='-')

    # Adding labels and title
    plt.xlabel('X-axis (every 500 units)')
    plt.ylabel('Y-axis')
    plt.title('Plot of Data Points')

    # Displaying the plot
    plt.show()


if __name__ == '__main__':

    cities = {
        0: (60, 200),
        1: (180, 200),
        2: (100, 180),
        3: (140, 180),
        4: (20, 160),
        5: (80, 160),
        6: (200, 160),
        7: (140, 140),
        8: (40, 120),
        9: (120, 120),
        10: (180, 100),
        11: (60, 80),
        12: (100, 80),
        13: (180, 60),
        14: (20, 40),
        15: (100, 40),
        16: (200, 40),
        17: (20, 20),
        18: (60, 20),
        19: (160, 20)
    }

    # cities = generate_cities(20, 1000, 1000)
    # with open("distances.pkl", 'rb') as file:
    #     cities = pickle.load(file)
    result, best_fitness, average_fitness = launch_algorithm(cities)
    display_path(result)
    display_average_fitness(average_fitness)
    # display_path([0, 4, 7, 8, 6, 5, 3, 2, 9, 1, 0])
    print(result, best_fitness)
    print(average_fitness)
