import math
import random
import time
import folium
from folium.plugins import PolyLineTextPath
from typing import List, Tuple

City = Tuple[float, float]
Tour = List[int]

def haversine(a: City, b: City) -> float:
    R = 6371  

    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    h = math.sin(dlat / 2) ** 2 + \
        math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2

    return 2 * R * math.atan2(math.sqrt(h), math.sqrt(1 - h))

def tour_length(tour: Tour, cities: List[City]) -> float:
    return sum(
        haversine(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
        for i in range(len(tour))
    )

def nearest_neighbor_random(cities: List[City], k: int = 3) -> Tour:
    unvisited = set(range(len(cities)))

    start = random.choice(list(unvisited))
    tour = [start]
    unvisited.remove(start)

    while unvisited:
        last = tour[-1]

        distances = sorted(
            [(i, haversine(cities[last], cities[i])) for i in unvisited],
            key=lambda x: x[1]
        )

        candidates = distances[:min(k, len(distances))]
        next_city = random.choice(candidates)[0]

        tour.append(next_city)
        unvisited.remove(next_city)

    return tour

def two_opt(tour: Tour, cities: List[City]) -> Tour:
    best = tour
    best_dist = tour_length(best, cities)

    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1:
                    continue

                new_tour = best[:]
                new_tour[i:j] = reversed(best[i:j])

                new_dist = tour_length(new_tour, cities)
                if new_dist < best_dist:
                    best = new_tour
                    best_dist = new_dist
                    improved = True

    return best

def print_simple_output(tour: Tour, names: List[str], cities: List[City]):
    path = " -> ".join(names[i] for i in tour)
    path += f" -> {names[tour[0]]}"

    print("\nBest Tour:")
    print(path)
    print("Total Distance:", round(tour_length(tour, cities), 2), "km")


def plot_map(cities: List[City], names: List[str], tour: Tour, filename: str):
    m = folium.Map(location=cities[tour[0]], zoom_start=6)

    for order, city_index in enumerate(tour):
        folium.Marker(
            location=cities[city_index],
            popup=f"{order + 1}. {names[city_index]}",
            tooltip=names[city_index],
            icon=folium.Icon(color="blue")
        ).add_to(m)

    for i in range(len(tour)):
        a = tour[i]
        b = tour[(i + 1) % len(tour)]

        line = folium.PolyLine(
            locations=[cities[a], cities[b]],
            color="red",
            weight=4
        ).add_to(m)

        PolyLineTextPath(
            line,
            " ➜➜ ",
            repeat=True,
            offset=8,
            attributes={
                "fill": "black",
                "font-weight": "900",
                "font-size": "18"
            }
        ).add_to(m)

    m.save(filename)
    print("Map with clear arrows saved:", filename)

print("Select number of cities:")
print("1 - 5 Cities")
print("2 - 15 Cities")
print("3 - 20 Cities")

choice = input("Your choice: ")

if choice == "1":
    from cities_5 import get_cities, get_city_names
    label = 5
elif choice == "2":
    from cities_15 import get_cities, get_city_names
    label = 15
elif choice == "3":
    from cities_20 import get_cities, get_city_names
    label = 20
else:
    raise ValueError("Invalid choice!")

cities = get_cities()
names = get_city_names()

start_time = time.perf_counter()

tour = nearest_neighbor_random(cities, k=3)
tour = two_opt(tour, cities)

end_time = time.perf_counter()
execution_time = end_time - start_time

print_simple_output(tour, names, cities)
print("Execution Time:", round(execution_time, 4), "seconds")

plot_map(cities, names, tour, f"tsp_random_{label}.html")
