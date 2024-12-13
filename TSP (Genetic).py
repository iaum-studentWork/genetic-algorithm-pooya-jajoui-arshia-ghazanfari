## TSM with Genetics

# importing dependencies
from random import randint as rnd
from random import shuffle
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Setting Parameters
N_CITIES = 8
WIDTH = 500
HEIGHT = 500

POPULATION_SIZE = 100
EPOCH = 200

# Random city generator function
def random_city_generator(n_c, a_w, a_h):
    offset = 20
    cities = []
    i = 0
    while i < n_c:
        city_location = [rnd(offset,a_w-offset), rnd(offset,a_h-offset)]
        if city_location not in cities:
            cities.append(city_location)
            i+=1
    return cities


# Initial Population function
def init_population(n, ps):
    population_list = []
    for i in range(ps):
        path = [i for i in range(n)]
        shuffle(path)
        path += [None]
        population_list.append(path)
    return population_list

# Cross Over Function (One-point Crossover)
def cross_over(population_list, n, p):
    for i in range(p):
        path = population_list[i][:n] + [None]
        population_list.append(path)
    return population_list

# Mutation Function (Swap Mutation)
def mutation(population_list, n, p):
    length = p*2
    i = p
    while i < length:
        cell1 = rnd(0,n-1)
        cell2 = rnd(0,n-1)
        if cell1 != cell2:
            population_list[i][cell1], population_list[i][cell2] = population_list[i][cell2], population_list[i][cell1]
            i+=1
    return population_list

#Fitness Function
def path_cordinates(cities_locations, path):
    cordinates = []
    for i in path:
        cordinates.append(cities_locations[i])
    return cordinates

def euclidean_distance(path):
    distance = 0
    for i in range(len(path)-1):
        distance += np.sqrt((path[i][0]-path[i+1][0])**2 + (path[i][1]-path[i+1][1])**2)
    return distance

def fitness(population_list, n, location_list):
    for i in range(len(population_list)):
        if population_list[i][-1]==None:
            current_path = path_cordinates(location_list, population_list[i][:n] + [population_list[i][0]])
            d = euclidean_distance(current_path)
            population_list[i][n] = d
    return population_list

# Sorter Function
def sorter(population_list, k):
    population_list.sort(key = lambda x: x[k])
    return population_list

# Draw Cities Function
def draw_cities(img, cities_locations, color):
    for x,y in cities_locations:
        img = cv2.circle(img, (x,y), 6, color, -1)
    return img

# Draw Path Function
def draw_path(img, path, color):
    for i in range(len(path)-1):
        img = cv2.line(img, path[i], path[i+1], color, 2)
    return img

# Main
if __name__ == "__main__":
    cities_locations = random_city_generator(N_CITIES, WIDTH, HEIGHT)
    current_population = init_population(N_CITIES, POPULATION_SIZE)

    for i in range(1, EPOCH+1):
        current_population = cross_over(current_population, N_CITIES, POPULATION_SIZE)
        current_population = mutation(current_population, N_CITIES, POPULATION_SIZE)
        current_population = fitness(current_population, N_CITIES, cities_locations)
        current_population = sorter(current_population, N_CITIES)
        current_population = current_population[:POPULATION_SIZE]
        # print("Best Path and Distance so far:", current_population[0])
    else:
        print("Best Found Solution:", current_population[0])
        area = np.full((WIDTH, HEIGHT, 3), 255, np.int16)
        area = draw_cities(area, cities_locations, (0,0,255))
        current_path = path_cordinates(cities_locations, current_population[0][:N_CITIES])
        current_path += [current_path[0]]
        area = draw_path(area, current_path, (187,134,192))
        plt.imshow(area)
        plt.grid()
        plt.show()