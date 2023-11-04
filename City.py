import random
import math


class City:
    def __init__(self, x, y, city_id):
        self.x = x
        self.y = y
        self.city_id = city_id

    def __str__(self):
        return f"city:{self.city_id} is at {self.x:.1f} : {self.y:.1f}"


def generate_cities(num_cities, space_width, space_height):
    cities = []
    city_id = 0
    for _ in range(num_cities):
        x = random.uniform(0, space_width)
        y = random.uniform(0, space_height)
        city = City(x, y, city_id)
        cities.append(city)
        city_id += 1
    return cities


def calculate_distance(city1, city2):
    x1 = city1.x
    y1 = city1.y
    x2 = city2.x
    y2 = city2.y
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def all_distances(cities):
    distances = []
    for city in cities:
        current_city_distances = []
        for dist_to_city in cities:
            current_city_distances.append(calculate_distance(city, dist_to_city))
        distances.append(current_city_distances)
    return distances
