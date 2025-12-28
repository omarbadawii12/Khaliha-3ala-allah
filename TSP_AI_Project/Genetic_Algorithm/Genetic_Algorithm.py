
import math
import time
import folium
from folium.features import DivIcon
from folium.plugins import PolyLineTextPath
import random

# =========================
# Cities Groups
# =========================

cities_5 = {
    "Cairo": [30.04, 31.23],
    "Alexandria": [31.20, 29.91],
    "Luxor": [25.68, 32.64],
    "Aswan": [24.08, 32.89],
    "Hurghada": [27.25, 33.81]
}

cities_15 = {
    **cities_5,
    "Suez": [29.96, 32.54],
    "Port Said": [31.26, 32.30],
    "Tanta": [30.78, 31.00],
    "Mansoura": [31.04, 31.37],
    "Ismailia": [30.59, 32.27],
    "Fayoum": [29.30, 30.84],
    "Minya": [28.09, 30.75],
    "Asyut": [27.17, 31.18],
    "Sohag": [26.55, 31.69],
    "Qena": [26.15, 32.71]
}

cities_20 = {
    **cities_15,
    "Sharm": [27.91, 34.32],
    "Matruh": [31.35, 27.23],
    "Zagazig": [30.58, 31.50],
    "Damietta": [31.41, 31.81],
    "Damanhur": [31.03, 30.47]
}

# =========================
# Distance Function
# =========================

def haversine(c1, c2):
    R = 6371  # km
    lat1, lon1 = map(math.radians, c1)
    lat2, lon2 = map(math.radians, c2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return R * (2 * math.asin(math.sqrt(a)))

def distance_matrix(cities):
    return [[haversine(cities[i], cities[j]) for j in range(len(cities))] for i in range(len(cities))]

# =========================
# Genetic Algorithm
# =========================

def create_population(size, N):
    return [random.sample(range(N), N) for _ in range(size)]

def fitness(tour, dist):
    return sum(dist[tour[i]][tour[(i+1)%len(tour)]] for i in range(len(tour)))

def selection(pop, dist):
    return min(random.sample(pop, 5), key=lambda x: fitness(x, dist))

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
    return tour

def genetic_algorithm(dist, N):
    start_time = time.time()  # بداية العد
    population = create_population(120, N)
    best = min(population, key=lambda x: fitness(x, dist))

    for _ in range(500):
        new_pop = [mutate(crossover(selection(population, dist), selection(population, dist))) for _ in range(120)]
        population = new_pop
        current = min(population, key=lambda x: fitness(x, dist))
        if fitness(current, dist) < fitness(best, dist):
            best = current

    exec_time = time.time() - start_time  # نهاية العد
    return best, fitness(best, dist), exec_time

# =========================
# Visualization (معدلة لإضافة العنوان الأنيق)
# =========================

def visualize(cities, names, tour, filename, num_cities):
    m = folium.Map(location=cities[tour[0]], zoom_start=6)

    for i, idx in enumerate(tour):
        # Marker with popup
        folium.Marker(
            cities[idx],
            popup=f"{names[idx]} (Step {i})",
            icon=folium.Icon(color="green" if i==0 else "blue", icon="info-sign")
        ).add_to(m)

        # Step numbers on map
        folium.map.Marker(
            cities[idx],
            icon=DivIcon(
                icon_size=(30,30),
                icon_anchor=(15,15),
                html=f'<div style="font-size:10px; font-weight:bold; color:black">{i}</div>'
            )
        ).add_to(m)

    # Path
    path = [cities[i] for i in tour] + [cities[tour[0]]]
    poly = folium.PolyLine(path, color="blue", weight=4, opacity=0.50).add_to(m)

    # Arrows along the path
    PolyLineTextPath(
        poly,
        "➜",
        repeat=250,  # أسهم أقل لتقليل التزاحم
        offset=6,
        attributes={"fill":"black","font-size":"12","font-weight":"bold"}
    ).add_to(m)

    # العنوان الجميل في أعلى يسار الخريطة (نفس الستايل في باقي الخوارزميات)
    title_html = f'''
        <div style="position: fixed; 
                    top: 10px; left: 50px; width: 500px; height: 80px; 
                    background-color: white; border:2px solid #1e3a8a; 
                    z-index:9999; font-size:24px; padding: 15px;
                    border-radius: 12px; box-shadow: 0 6px 12px rgba(0,0,0,0.3);
                    font-weight: bold; text-align: center; line-height: 1.4; color: #1e3a8a;">
            <b>Genetic Algorithm (GA)</b><br>
            Traveling Salesman Problem (TSP) - {num_cities} Cities
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))

    m.save(filename)
    print(f"\nMap saved as {filename}")

if __name__ == "__main__":
    choice = input("Choose number of cities (5 / 15 / 20): ")
    if choice=="5":
        selected=cities_5
        num_cities = 5
    elif choice=="15":
        selected=cities_15
        num_cities = 15
    elif choice=="20":
        selected=cities_20
        num_cities = 20
    else:
        raise ValueError("Invalid choice")

    names = list(selected.keys())
    cities = list(selected.values())
    N = len(cities)

    dist = distance_matrix(cities)
    best_tour, cost, exec_time = genetic_algorithm(dist, N)

    print("\nBest Tour (Random Start):")
    for i in best_tour:
        print(names[i], end=" → ")
    print(names[best_tour[0]])

    print(f"\nTotal Distance: {cost:.2f} km")
    print(f"Execution Time: {exec_time:.4f} seconds")

    visualize(cities, names, best_tour, f"tsp_{choice}_cities.html", num_cities)