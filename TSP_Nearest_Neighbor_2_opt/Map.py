import math
import time
import tracemalloc
import folium
from folium import plugins
from typing import List, Tuple
from dataclasses import dataclass

# ================== Type Definitions ==================
City = Tuple[float, float]   # (latitude, longitude)
Tour = List[int]

# ================== Result Structure ==================
@dataclass
class AlgorithmResult:
    name: str
    path_cost: float
    execution_time: float
    memory_kb: float
    improvement: float

# ================== Distance Function (Haversine) ==================
def haversine_distance(city_a: City, city_b: City) -> float:
    R = 6371  # Radius of Earth in kilometers

    lat1, lon1 = map(math.radians, city_a)
    lat2, lon2 = map(math.radians, city_b)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + \
        math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# ================== Tour Length ==================
def compute_tour_length(tour: Tour, cities: List[City]) -> float:
    total = 0.0
    for i in range(len(tour)):
        total += haversine_distance(
            cities[tour[i]],
            cities[tour[(i + 1) % len(tour)]]
        )
    return total

# ================== TSP Algorithms ==================
def nearest_neighbor(cities: List[City], start_city: int) -> Tour:
    unvisited = set(range(len(cities)))
    tour = [start_city]
    unvisited.remove(start_city)

    while unvisited:
        current = tour[-1]
        nearest = min(
            unvisited,
            key=lambda c: haversine_distance(cities[current], cities[c])
        )
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

def nn_2opt_solver(cities, start_index):
    initial = nearest_neighbor(cities, start_index)
    optimized = two_opt(initial, cities)
    return optimized

# ================== Algorithm Runner ==================
def run_algorithm(name, solver_func, cities, start_index, baseline_cost=None):
    tracemalloc.start()
    start_time = time.perf_counter()

    tour = solver_func(cities, start_index)

    exec_time = time.perf_counter() - start_time
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    cost = compute_tour_length(tour, cities)

    improvement = 0.0
    if baseline_cost:
        improvement = ((baseline_cost - cost) / baseline_cost) * 100

    return tour, AlgorithmResult(
        name=name,
        path_cost=cost,
        execution_time=exec_time,
        memory_kb=peak / 1024,
        improvement=improvement
    )

# ================== Map Visualization ==================
def create_map(cities, city_names, tour, filename, title, color):
    avg_lat = sum(c[0] for c in cities) / len(cities)
    avg_lon = sum(c[1] for c in cities) / len(cities)

    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=6, tiles="CartoDB positron")

    for i, (lat, lon) in enumerate(cities):
        folium.Marker(
            location=[lat, lon],
            popup=city_names[i],
            icon=folium.Icon(color="black")
        ).add_to(m)

    path = [cities[i] for i in tour] + [cities[tour[0]]]
    poly = folium.PolyLine(path, color=color, weight=5).add_to(m)

    plugins.PolyLineTextPath(
        poly, " ➜ ", repeat=True, offset=7,
        attributes={"fill": "red", "font-size": "18"}
    ).add_to(m)

    m.get_root().html.add_child(
        folium.Element(f"<h3 align='center'>{title}</h3>")
    )

    m.save(filename)

# ================== City Data ==================
ALL_CITIES = {
    "Cairo": (30.044, 31.23),
    "Alexandria": (31.20, 29.91),
    "Luxor": (25.68, 32.64),
    "Aswan": (24.08, 32.89),
    "Hurghada": (27.25, 33.81),
    "Suez": (29.96, 32.54),
    "Port Said": (31.26, 32.30),
    "Tanta": (30.78, 31.00),
    "Mansoura": (31.04, 31.37),
    "Ismailia": (30.59, 32.27),
    "Fayoum": (29.30, 30.84),
    "Minya": (28.09, 30.75),
    "Asyut": (27.17, 31.18),
    "Sohag": (26.55, 31.69),
    "Qena": (26.15, 32.71),
    "Sharm": (27.91, 34.32),
    "Matruh": (31.35, 27.23),
    "Zagazig": (30.58, 31.50),
    "Damietta": (31.41, 31.81),
    "Damanhur": (31.03, 30.47),

}

# ================== Main ==================
def main():
    while True:
        try:
            n = int(input("Enter number of cities (5–20): "))
            if 5 <= n <= 20:
                break
        except ValueError:
            pass

    city_names = list(ALL_CITIES.keys())[:n]
    cities = list(ALL_CITIES.values())[:n]

    print("\nAvailable Cities:")
    for name in city_names:
        print("-", name)

    while True:
        start_name = input("\nEnter starting city: ").strip().lower()
        if start_name in [c.lower() for c in city_names]:
            start_index = [c.lower() for c in city_names].index(start_name)
            start_city = city_names[start_index]
            break

    # ===== Baseline NN =====
    nn_tour, nn_result = run_algorithm(
        "Nearest Neighbor (Baseline)",
        lambda c, s: nearest_neighbor(c, s),
        cities,
        start_index
    )

    # ===== NN + 2-opt =====
    nn2opt_tour, nn2opt_result = run_algorithm(
        "Nearest Neighbor + 2-opt",
        nn_2opt_solver,
        cities,
        start_index,
        baseline_cost=nn_result.path_cost
    )

    results = [nn_result, nn2opt_result]

    # ===== Comparison Table =====
    print("\n================ ALGORITHM COMPARISON ================")
    print(f"{'Algorithm':30} {'Cost (km)':>12} {'Time(s)':>10} {'Memory(KB)':>12} {'Improve%':>10}")
    print("-" * 85)
    for r in results:
        print(f"{r.name:30} {r.path_cost:12.2f} {r.execution_time:10.4f} "
              f"{r.memory_kb:12.2f} {r.improvement:10.2f}")

    # ===== Maps =====
    create_map(cities, city_names, nn_tour,
               "baseline_nn.html",
               f"Nearest Neighbor (Start: {start_city})",
               "blue")

    create_map(cities, city_names, nn2opt_tour,
               "nn_2opt.html",
               f"Nearest Neighbor + 2-opt (Start: {start_city})",
               "green")

if __name__ == "__main__":
    main()
