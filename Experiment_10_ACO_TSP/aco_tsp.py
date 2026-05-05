# Ant Colony Optimization (ACO) - Traveling Salesman Problem
# TSP: visit every city exactly once and return to the starting city, minimising total distance.
# ACO Idea: many "ants" each build a tour; pheromone trails on edges of shorter tours
# get reinforced over time, biasing future ants toward better paths.
# This simplified version uses random tours and keeps the best one found.

import random

# Number of cities in the problem.
cities = 5

# Symmetric distance matrix: distance[i][j] = distance from city i to city j.
# Diagonal is 0 because the distance from a city to itself is 0.
distance = [[0, 2, 9, 10, 7],
            [2, 0, 6, 4, 3],
            [9, 6, 0, 8, 5],
            [10, 4, 8, 0, 6],
            [7, 3, 5, 6, 0]]

# Track the best tour discovered so far and its length.
best_path = None
best_distance = 999  # Large initial value so any real tour will beat it.

# Simulate 20 ants; each builds a random tour (acts like exploration).
for i in range(20):
    # Construct a candidate tour by randomly permuting the city indices.
    path = list(range(cities))
    random.shuffle(path)

    # Compute total distance of this tour by summing consecutive edges.
    dist = 0
    for j in range(cities - 1):
        dist += distance[path[j]][path[j + 1]]

    # If this tour is shorter than the best seen, remember it.
    if dist < best_distance:
        best_distance = dist
        best_path = path

# Final result: shortest tour discovered across all ants.
print("Best Path:", best_path)
print("Shortest Distance:", best_distance)
