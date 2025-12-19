import math
import folium
from folium import plugins
from typing import List, Tuple

# ================== Type Definitions ==================
City = Tuple[float, float]
Tour = List[int]

# ================== Distance ==================
def euclidean_distance(city_a: City, city_b: City) -> float:
    return math.sqrt((city_a[0] - city_b[0]) ** 2 + (city_a[1] - city_b[1]) ** 2)

def compute_tour_length(tour: Tour, cities: List[City]) -> float:
    total = 0.0
    for i in range(len(tour)):
        total += euclidean_distance(
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
            key=lambda c: euclidean_distance(cities[current], cities[c])
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

# ================== Map ==================
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
    print(f"✔ Generated: {filename}")

# ================== City Data ==================
ALL_CITIES = {
    "Cairo": (30.04, 31.23),
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
    "Damanhur": (31.03, 30.47)
}

# ================== Main ==================
def main():
    while True:
        try:
            n = int(input("Enter number of cities (5–20): "))
            if 5 <= n <= 20:
                break
            print(" Choose between 5 and 20")
        except ValueError:
            print(" Enter a valid number")

    city_names = list(ALL_CITIES.keys())[:n]
    cities = list(ALL_CITIES.values())[:n]

    print("\nAvailable Cities:")
    for name in city_names:
        print(f"- {name}")

    while True:
        start_name = input("\nEnter starting city name: ").strip().lower()
        if start_name in [c.lower() for c in city_names]:
            start_index = [c.lower() for c in city_names].index(start_name)
            start_city_name = city_names[start_index]
            break
        print(" City not found, try again")

    initial_tour = nearest_neighbor(cities, start_index)
    optimized_tour = two_opt(initial_tour, cities)

    print("\nRESULTS")
    print(f"Starting City: {start_city_name}")
    print(f"Initial Distance: {compute_tour_length(initial_tour, cities):.2f}")
    print(f"Optimized Distance: {compute_tour_length(optimized_tour, cities):.2f}")

    create_map(
        cities, city_names, initial_tour,
        "initial_tour.html",
        f"Initial Tour (Start: {start_city_name})",
        "blue"
    )

    create_map(
        cities, city_names, optimized_tour,
        "optimized_tour.html",
        f"Optimized Tour (Start: {start_city_name})",
        "green"
    )

if __name__ == "__main__":
    main()
