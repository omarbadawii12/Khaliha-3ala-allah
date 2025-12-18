import math
from data.cities import tour_cost

def nn_2opt_tsp(dist):
    """Nearest Neighbor followed by 2-opt."""
    n = len(dist)
    visited = [False] * n
    tour = [0]  # Start at city 0
    visited[0] = True
    current = 0

    while len(tour) < n:
        nearest = None
        min_dist = math.inf
        for city in range(n):
            if not visited[city] and dist[current][city] < min_dist:
                min_dist = dist[current][city]
                nearest = city
        current = nearest
        tour.append(current)
        visited[current] = True

    # Apply 2-opt
    tour = two_opt(tour, dist)
    tour.append(tour[0])  # Close the tour
    cost = tour_cost(tour, dist)
    return tour, cost

def two_opt(route, dist):
    """2-opt optimization."""
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue
                if cost_change(dist, route[i - 1], route[i], route[j - 1], route[j]) < 0:
                    route[i:j] = route[j - 1:i - 1:-1]
                    improved = True
    return route

def cost_change(dist, n1, n2, n3, n4):
    return dist[n1][n3] + dist[n2][n4] - dist[n1][n2] - dist[n3][n4]