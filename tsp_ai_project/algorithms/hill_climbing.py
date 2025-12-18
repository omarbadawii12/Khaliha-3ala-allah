import random
import numpy as np
from data.cities import tour_cost

def get_neighbors(tour):
    neighbors = []
    n = len(tour)
    for i in range(n):
        for j in range(i + 1, n):
            neighbor = tour.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def hill_climbing_tsp(dist, restarts=10):
    """Hill Climbing with random restarts."""
    n = len(dist)
    best_tour = None
    best_cost = float('inf')

    for _ in range(restarts):
        current_tour = list(range(n))
        random.shuffle(current_tour)
        current_cost = tour_cost(current_tour, dist)

        while True:
            neighbors = get_neighbors(current_tour)
            best_neighbor = min(neighbors, key=lambda t: tour_cost(t, dist))
            neighbor_cost = tour_cost(best_neighbor, dist)
            if neighbor_cost >= current_cost:
                break
            current_tour = best_neighbor
            current_cost = neighbor_cost

        if current_cost < best_cost:
            best_cost = current_cost
            best_tour = current_tour + [current_tour[0]]

    return best_tour, best_cost