import random
import math
import time
import folium

# =========================
# City & Distance Utilities
# =========================

def generate_city_coordinates(N):
    random.seed(42)
    # Lat, Lon (قريبة من مصر عشان شكل الخريطة يكون حلو)
    base_lat, base_lon = 30.0, 31.0
    return [
        (base_lat + random.uniform(-0.5, 0.5),
         base_lon + random.uniform(-0.5, 0.5))
        for _ in range(N)
    ]


def calculate_distance_matrix(cities):
    N = len(cities)
    matrix = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            lat1, lon1 = cities[i]
            lat2, lon2 = cities[j]
            matrix[i][j] = math.sqrt((lat1-lat2)**2 + (lon1-lon2)**2)
    return matrix


# =========================
# Genetic Algorithm
# =========================

def create_population(size, N):
    pop = []
    base = list(range(N))
    for _ in range(size):
        random.shuffle(base)
        pop.append(base[:])
    return pop


def fitness(tour, dist):
    return sum(dist[tour[i]][tour[(i+1) % len(tour)]] for i in range(len(tour)))


def selection(pop, dist):
    candidates = random.sample(pop, 5)
    candidates.sort(key=lambda x: fitness(x, dist))
    return candidates[0]


def crossover(p1, p2):
    size = len(p1)
    a, b = sorted(random.sample(range(size), 2))
    child = [-1]*size
    child[a:b] = p1[a:b]
    ptr = 0
    for city in p2:
        if city not in child:
            while child[ptr] != -1:
                ptr += 1
            child[ptr] = city
    return child


def mutate(tour, rate=0.02):
    if random.random() < rate:
        i, j = random.sample(range(len(tour)), 2)
        tour[i], tour[j] = tour[j], tour[i]


def genetic_algorithm(dist, N, pop_size=100, generations=400):
    population = create_population(pop_size, N)
    best = min(population, key=lambda x: fitness(x, dist))

    for _ in range(generations):
        new_pop = []
        for _ in range(pop_size):
            p1 = selection(population, dist)
            p2 = selection(population, dist)
            child = crossover(p1, p2)
            mutate(child)
            new_pop.append(child)
        population = new_pop
        current_best = min(population, key=lambda x: fitness(x, dist))
        if fitness(current_best, dist) < fitness(best, dist):
            best = current_best

    return best, fitness(best, dist)


# =========================
# Google Maps-style Visualization
# =========================

def visualize_on_map(cities, tour, filename="tsp_map.html"):
    start_city = tour[0]
    center = cities[start_city]

    m = folium.Map(location=center, zoom_start=10)

    # رسم المدن مع الترتيب
    for order, city_index in enumerate(tour):
        lat, lon = cities[city_index]

        if order == 0:
            color = "green"   # نقطة البداية
        else:
            color = "blue"

        folium.Marker(
            location=[lat, lon],
            popup=f"City {city_index} (Step {order})",
            icon=folium.Icon(color=color, icon="flag")
        ).add_to(m)

        # رقم الزيارة
        folium.map.Marker(
            [lat, lon],
            icon=folium.DivIcon(
                html=f"""
                <div style="font-size: 12pt;
                            color: black;
                            font-weight: bold;">
                    {order}
                </div>
                """
            )
        ).add_to(m)

    # الرجوع لنقطة البداية
    full_path = tour + [start_city]
    route = [cities[i] for i in full_path]

    # رسم المسار
    folium.PolyLine(
        locations=route,
        color="red",
        weight=4,
        opacity=0.8
    ).add_to(m)

    # إضافة الأسهم (Direction)
    for i in range(len(route) - 1):
        folium.PolyLine(
            locations=[route[i], route[i + 1]],
            color="red",
            weight=4,
            opacity=0.8,
            tooltip=f"{i} → {i+1}"
        ).add_to(m)

    m.save(filename)
    print(f"\nDirectional map saved as {filename}")



# =========================
# Main
# =========================

if __name__ == "__main__":
    N = int(input("Enter number of cities (5 / 15 / 20): "))

    cities = generate_city_coordinates(N)
    dist_matrix = calculate_distance_matrix(cities)

    start = time.time()
    best_tour, best_cost = genetic_algorithm(dist_matrix, N)
    end = time.time()

    print("Best tour:", best_tour)
    print("Cost:", round(best_cost, 4))
    print("Execution Time:", round(end - start, 4), "seconds")

    visualize_on_map(cities, best_tour, f"tsp_{N}_cities.html")
