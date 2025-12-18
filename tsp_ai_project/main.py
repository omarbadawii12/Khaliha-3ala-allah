from data.cities import generate_cities, compute_distances
from algorithms.ucs import ucs_tsp
from algorithms.a_star_search import a_star_tsp
from algorithms.hill_climbing import hill_climbing_tsp
from algorithms.nearest_neighbor import nn_2opt_tsp
from algorithms.genetic_algorithm import ga_tsp
from utils.visualization import plot_tour
from utils.comparison import compare_algorithms

# Default: 10 cities for exact methods (UCS, A* are slow for larger)
num_cities = 10
cities = generate_cities(num_cities)
dist = compute_distances(cities)

algorithms = {
    'UCS': ucs_tsp,
    'A*': a_star_tsp,
    'Hill Climbing': hill_climbing_tsp,
    'Nearest Neighbor + 2-opt': nn_2opt_tsp,
    'Genetic Algorithm': ga_tsp
}

results = compare_algorithms(algorithms, cities, dist)

# Print results
print("Performance Comparison:")
for name, res in results.items():
    print(f"{name}: Cost = {res['cost']:.2f}, Time = {res['time']:.4f} seconds")

# Visualize
for name, res in results.items():
    plot_tour(cities, res['tour'], name)

print("Visualizations saved in 'results' folder.")