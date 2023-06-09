from itertools import compress
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations


from data import *


def initial_population(individual_size, population_size):
    return [[random.choice([True, False]) for _ in range(individual_size)] for _ in range(population_size)]


def fitness(items, knapsack_max_capacity, individual):
    total_weight = sum(compress(items['Weight'], individual))
    if total_weight > knapsack_max_capacity:
        return 0
    return sum(compress(items['Value'], individual))


def population_best(items, knapsack_max_capacity, population):
    best_individual = None
    best_individual_fitness = -1
    for individual in population:
        individual_fitness = fitness(items, knapsack_max_capacity, individual)
        if individual_fitness > best_individual_fitness:
            best_individual = individual
            best_individual_fitness = individual_fitness
    return best_individual, best_individual_fitness


def population_elites(population, elites, n_elites):
    for _ in range(n_elites):
        elite, _  = population_best(items,knapsack_max_capacity, population)
        population.remove(elite)
        elites.append(elite)


def get_population_fitness(population):
    pop_fitness = 0
    for individual in population:
        pop_fitness += fitness(items, knapsack_max_capacity, individual)
    return pop_fitness


def get_probability(individual, population_fitness):
    individual_fitness = fitness(items, knapsack_max_capacity, individual)
    return individual_fitness / population_fitness


def random_individual(probabilities):
    rand = random.randint(0, 99999999)/ 100000000
    weight_sum = 0.0
    for index, probability in enumerate(probabilities):
        weight_sum += probability
        if weight_sum > rand:
            return population[index]
    return population[0]


def get_parents(population):
    probabilities = list()
    population_fitness = get_population_fitness(population)
    for individual in population:
        probabilities.append(get_probability(individual, population_fitness))
    parents = list()

    for _ in range(n_selection):
        parents.append(random_individual(probabilities))

    return parents


def split_half_dna(parent, pivot):
    parent_parts = []
    parent_parts.append(parent[:pivot])
    parent_parts.append(parent[pivot:])
    return parent_parts


def get_children(parent_a, parent_b):
    pivot = random.randint(1, len(parent_a))
    parent_part_a = split_half_dna(parent_a, pivot)
    parent_part_b = split_half_dna(parent_b, pivot)
    child_part_a = parent_part_a[0] + parent_part_b[1]
    child_part_b = parent_part_b[0] + parent_part_a[1]
    return child_part_a, child_part_b


def create_children(parents):
    children = []
    pairs = list(combinations(parents, 2))
    for pair in pairs:
        child_a, child_b = get_children(pair[0], pair[1])
        children.append(child_a)
        children.append(child_b)
    return children


def mutate_children(children):
    for i, child in enumerate(children):
        mutation = random.randint(0, len(child) -1)
        child[mutation] = not child[mutation]
        children[i] = child 


items, knapsack_max_capacity = get_big()
print(items)

population_size = 96
generations = 200
n_selection = 20
n_elite = 4

start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []
population = initial_population(len(items), population_size)
for _ in range(generations):
    population_history.append(population)
    best_individuals = []
    # TODO: implement genetic algorithm
    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)
    if best_individual_fitness > best_fitness:
        best_solution = best_individual
        best_fitness = best_individual_fitness
    best_history.append(best_fitness)
    best_individuals.append(best_individual)
    
    pop_copy = population.copy()
    pop_copy.remove(best_individual)
    population_elites(pop_copy, best_individuals, n_elite) 
    parents = get_parents(population)
    children = create_children(parents)
    mutate_children(children)
    population = children
    population = population + best_individuals


end_time = time.time()
total_time = end_time - start_time
print('Best solution:', list(compress(items['Name'], best_solution)))
print('Best solution value:', best_fitness)
print('Time: ', total_time)

# plot generations
x = []
y = []
top_best = 10
for i, population in enumerate(population_history):
    plotted_individuals = min(len(population), top_best)
    x.extend([i] * plotted_individuals)
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    population_fitnesses.sort(reverse=True)
    y.extend(population_fitnesses[:plotted_individuals])
plt.scatter(x, y, marker='.')
plt.plot(best_history, 'r')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()
