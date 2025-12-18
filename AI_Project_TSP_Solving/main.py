import math
from typing import List, Tuple
import matplotlib.pyplot as plt

# Type Definitions
City = Tuple[float, float]
Tour = List[int]

# Distance Calculation
def euclidean_distance(city_a: City, city_b: City) -> float:
    """
    Compute the Euclidean distance between two cities.
    """
    return math.sqrt(
        (city_a[0] - city_b[0]) ** 2 +
        (city_a[1] - city_b[1]) ** 2
    )

# Tour Distance Calculation
# ================================
def compute_tour_length(tour: Tour, cities: List[City]) -> float:
    """
    Compute the total length of a TSP tour.
    """
    total = 0.0
    for i in range(len(tour)):
        total += euclidean_distance(
            cities[tour[i]],
            cities[tour[(i + 1) % len(tour)]]
        )
    return total

# Nearest Neighbor Algorithm
def nearest_neighbor(cities: List[City], start_city: int = 0) -> Tour:
    """
    Generate an initial TSP tour using the Nearest Neighbor heuristic.
    """
    unvisited = set(range(len(cities)))
    tour = [start_city]
    unvisited.remove(start_city)

    while unvisited:
        current = tour[-1]
        nearest = min(
            unvisited,
            key=lambda city_index: euclidean_distance(
                cities[current],
                cities[city_index]
            )
        )
        tour.append(nearest)
        unvisited.remove(nearest)

    return tour

# 2-opt Optimization Algorithm

def two_opt(tour: Tour, cities: List[City]) -> Tour:
    """
    Improve a TSP tour using the 2-opt local search algorithm.
    """
    best_distance = compute_tour_length(tour, cities)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1:
                    continue  # Skip adjacent edges

                candidate = tour[:]
                candidate[i:j] = reversed(tour[i:j])
                candidate_distance = compute_tour_length(candidate, cities)

                if candidate_distance < best_distance:
                    tour = candidate
                    best_distance = candidate_distance
                    improved = True

        if improved:
            break

    return tour

# Visualization with Directions
def plot_tour_with_direction(cities: List[City], tour: Tour, title: str):
    """
    Visualize the TSP tour with directional arrows.
    """
    plt.figure(figsize=(8, 6))

    # Plot cities
    x_coords = [city[0] for city in cities]
    y_coords = [city[1] for city in cities]
    plt.scatter(x_coords, y_coords, s=120)

    # Label cities
    for i, (x, y) in enumerate(cities):
        plt.text(x + 0.1, y + 0.1, str(i), fontsize=12, fontweight='bold')

    # Draw directional arrows
    for i in range(len(tour)):
        start = cities[tour[i]]
        end = cities[tour[(i + 1) % len(tour)]]

        dx = end[0] - start[0]
        dy = end[1] - start[1]

        plt.arrow(
            start[0], start[1],
            dx, dy,
            length_includes_head=True,
            head_width=0.15,
            head_length=0.2,
            alpha=0.8
        )

    plt.title(title)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()

# Main Execution
def main():
    """
    cities: List[City] = [
        (0, 0),
        (2, 6),
        (5, 2),
        (6, 6),
        (8, 3)
    ]
    """
    """
    cities = [
        (2, 1),  # 0
        (8, 1),  # 1
        (1, 3),  # 2
        (5, 3),  # 3
        (9, 4),  # 4
        (3, 5),  # 5
        (7, 5),  # 6
        (1, 7),  # 7
        (4, 7),  # 8
        (8, 7),  # 9
        (2, 9),  # 10
        (6, 9),  # 11
    ]
    """
    """
    cities = [
        (1, 1),  # 0
        (6, 1),  # 1
        (11, 1),  # 2

        (3, 3),  # 3
        (9, 3),  # 4
        (5, 4),  # 5

        (1, 5),  # 6
        (7, 5),  # 7
        (11, 6),  # 8

        (3, 7),  # 9
        (9, 7),  # 10

        (5, 9),  # 11
        (1, 10),  # 12
        (7, 10),  # 13
        (11, 9)  # 14
    ]
  """
    """"
    cities = [
        (5, 5),  # 0
        (1, 4),  # 1
        (3, 11),  # 2
        (16, 2),  # 3
        (2, 16),  # 4
        (7, 9),  # 5
        (9, 7),  # 6
        (8, 11),  # 7
        (6, 8),  # 8
        (15, 10),  # 9
        (14, 1),  # 10
        (17, 3),  # 11
        (6, 11),  # 12
        (13, 4),  # 13
        (5, 6),  # 14
        (6, 3),  # 15
        (19, 4),  # 16
        (5, 17),  # 17
        (11, 6),  # 18
        (8, 5)  # 19
    ]
    """
    cities = [
        (2, 9), (5, 8), (8, 9), (1, 6), (4, 6),
        (7, 6), (10, 6), (2, 4), (5, 4), (8, 4),
        (0, 2), (3, 2), (6, 2), (9, 2), (12, 2),
        (5, 0), (10, 0), (15, 5), (15, 10), (12, 8)
    ]

    print("\nTRAVELING SALESMAN PROBLEM (TSP)")
    print("Solution using Nearest Neighbor + 2-opt\n")

    initial_tour = nearest_neighbor(cities, start_city=0)
    optimized_tour = two_opt(initial_tour, cities)

    print("Initial Tour:", initial_tour)
    print("Initial Distance:", round(compute_tour_length(initial_tour, cities), 2))

    print("\nOptimized Tour:", optimized_tour)
    print("Optimized Distance:", round(compute_tour_length(optimized_tour, cities), 2))

    # Visualization (Simulation)
    plot_tour_with_direction(
        cities,
        initial_tour,
        "Initial Tour (Nearest Neighbor) - Directional"
    )

    plot_tour_with_direction(
        cities,
        optimized_tour,
        "Optimized Tour (2-opt) - Directional"
    )

if __name__ == "__main__":
    main()