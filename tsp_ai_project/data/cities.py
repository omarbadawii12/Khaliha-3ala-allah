import numpy as np

def generate_cities(num_cities):
    """Generate random city coordinates in 2D plane."""
    return np.random.rand(num_cities, 2) * 100  # Points in [0, 100] x [0, 100]

def compute_distances(cities):
    """Compute Euclidean distance matrix between cities."""
    num_cities = len(cities)
    dist = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            distance = np.linalg.norm(cities[i] - cities[j])
            dist[i, j] = distance
            dist[j, i] = distance
    return dist

def tour_cost(tour, dist):
    """Calculate the total cost of a tour."""
    cost = 0
    for i in range(len(tour) - 1):
        cost += dist[tour[i], tour[i + 1]]
    cost += dist[tour[-1], tour[0]]  # Return to start
    return cost