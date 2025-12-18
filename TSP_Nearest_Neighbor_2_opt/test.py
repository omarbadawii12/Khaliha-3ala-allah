import math
import folium
from folium import plugins
from typing import List, Tuple

# Type Definitions
City = Tuple[float, float]
Tour = List[int]

# Distance Calculation
def euclidean_distance(city_a: City, city_b: City) -> float:
    return math.sqrt((city_a[0] - city_b[0]) ** 2 + (city_a[1] - city_b[1]) ** 2)


def compute_tour_length(tour: Tour, cities: List[City]) -> float:
    total = 0.0
    for i in range(len(tour)):
        total += euclidean_distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
    return total


# TSP Algorithms

def nearest_neighbor(cities: List[City], start_city: int = 0) -> Tour:
    unvisited = set(range(len(cities)))
    tour = [start_city]
    unvisited.remove(start_city)
    while unvisited:
        current = tour[-1]
        nearest = min(unvisited, key=lambda c: euclidean_distance(cities[current], cities[c]))
        tour.append(nearest)
        unvisited.remove(nearest)
    return tour


def two_opt(tour: Tour, cities: List[City]) -> Tour:
    best_distance = compute_tour_length(tour, cities)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 1):
            for j in range(i + 1, len(tour)):
                new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
                new_distance = compute_tour_length(new_tour, cities)
                if new_distance < best_distance:
                    tour = new_tour
                    best_distance = new_distance
                    improved = True
      
    return tour


# Visualization Function

def create_map(cities: List[City], tour: Tour, filename: str, title: str, line_color: str):
    avg_lat = sum(c[0] for c in cities) / len(cities)
    avg_lon = sum(c[1] for c in cities) / len(cities)

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=6, tiles='CartoDB positron')

    # Add Markers
    for i, (lat, lon) in enumerate(cities):
        folium.Marker(
            location=[lat, lon],
            popup=f"City {i}",
            icon=folium.Icon(color='black', icon='info-sign')
        ).add_to(m)

    # Path coordinates
    path_coords = [cities[i] for i in tour]
    path_coords.append(cities[tour[0]])

    # Draw Line
    path_line = folium.PolyLine(
        locations=path_coords,
        color=line_color,
        weight=5,
        opacity=0.7
    ).add_to(m)

    # Add Directional Arrows
    plugins.PolyLineTextPath(
        path_line,
        ' \u27A4 ',  
        repeat=True,
        offset=8,
        attributes={'fill': 'red', 'font-weight': 'bold', 'font-size': '24'}
    ).add_to(m)

    # Add Title to Map
    title_html = f'<h3 align="center" style="font-size:20px"><b>{title}</b></h3>'
    m.get_root().html.add_child(folium.Element(title_html))

    m.save(filename)
    print(f"Generated: {filename}")


# Main Execution
def main():
   
    cities = [
        (30.0444, 31.2357), (31.2001, 29.9187),
        (24.0889, 32.8998), (25.6872, 32.6396),
        (27.2579, 33.8116), (31.0409, 31.3785),
        (27.1783, 31.1859), (28.5092, 34.5138),
        (29.3084, 30.8428), (31.2565, 32.2841)
    ]

    # 1. Initial Solution
    initial_tour = nearest_neighbor(cities)
    initial_dist = compute_tour_length(initial_tour, cities)

    # 2. Optimized Solution
    optimized_tour = two_opt(initial_tour, cities)
    optimized_dist = compute_tour_length(optimized_tour, cities)

    print(f"\nRESULTS:")
    print(f"Initial Distance (Nearest Neighbor): {initial_dist:.2f}")
    print(f"Optimized Distance (2-opt): {optimized_dist:.2f}")
    print(f"Improvement: {((initial_dist - optimized_dist) / initial_dist) * 100:.2f}%")

    # 3. Create both maps for comparison
    create_map(cities, initial_tour, "1_initial_tour.html", "Initial Tour (Nearest Neighbor)", "blue")
    create_map(cities, optimized_tour, "2_optimized_tour.html", "Optimized Tour (2-opt Applied)", "green")


if __name__ == "__main__":

    main()
