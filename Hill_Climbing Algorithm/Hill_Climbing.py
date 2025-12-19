import random, math, folium, webbrowser, os, time


# Distance Functions

def haversine(c1, c2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [c1[0], c1[1], c2[0], c2[1]])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def total_distance(route, coords):
    return sum(
        haversine(coords[route[i]], coords[route[(i+1) % len(route)]])
        for i in range(len(route))
    )


# Hill Climbing Algorithm

def hill_climbing(coords):
    n = len(coords)

    # Random initial solution
    current_route = list(range(n))
    random.shuffle(current_route)
    current_cost = total_distance(current_route, coords)

    while True:
        best_neighbor = current_route
        best_cost = current_cost

        for i in range(n):
            for j in range(i + 1, n):
                neighbor = current_route[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                cost = total_distance(neighbor, coords)

                if cost < best_cost:
                    best_neighbor, best_cost = neighbor, cost

        if best_cost >= current_cost:
            break

        current_route, current_cost = best_neighbor, best_cost

    return current_route, current_cost


# Cities (Fixed Order)

cities = {
    "Cairo": [30.04, 31.23],
    "Alexandria": [31.20, 29.91],
    "Luxor": [25.68, 32.64],
    "Aswan": [24.08, 32.89],
    "Hurghada": [27.25, 33.81],
    "Suez": [29.96, 32.54],
    "Port Said": [31.26, 32.30],
    "Tanta": [30.78, 31.00],
    "Mansoura": [31.04, 31.37],
    "Ismailia": [30.59, 32.27],
    "Fayoum": [29.30, 30.84],
    "Minya": [28.09, 30.75],
    "Asyut": [27.17, 31.18],
    "Sohag": [26.55, 31.69],
    "Qena": [26.15, 32.71],
    "Sharm": [27.91, 34.32],
    "Matruh": [31.35, 27.23],
    "Zagazig": [30.58, 31.50],
    "Damietta": [31.41, 31.81],
    "Damanhur": [31.03, 30.47]
}


# USER INPUT

NUM_CITIES = int(input("Enter number of cities (5 - 20): "))
RESTARTS = int(input("Enter number of restarts: "))

if NUM_CITIES < 5 or NUM_CITIES > 20:
    raise ValueError("Number of cities must be between 5 and 20")

names = list(cities.keys())[:NUM_CITIES]
coords = list(cities.values())[:NUM_CITIES]


# Run Hill Climbing with Restarts + Seed

print(f"\n--- Running TSP using Hill Climbing ({NUM_CITIES} Cities) ---")

start_time = time.time()
best_route, best_dist = None, float('inf')

for r_id in range(RESTARTS):
    
    random.seed(time.time() + r_id)

    route, dist = hill_climbing(coords)

    if dist < best_dist:
        best_route, best_dist = route, dist

end_time = time.time()


# Output

print("\n" + "=" * 60)
print(f"Execution Time : {end_time - start_time:.4f} sec")
print(f"Best Distance : {best_dist:.2f} km")
print("Best Path     :")
print(" -> ".join([names[i] for i in best_route]) + f" -> {names[best_route[0]]}")
print("=" * 60)


# Map Visualization

m = folium.Map(location=coords[best_route[0]], zoom_start=6)

for i, idx in enumerate(best_route):
    color = 'green' if i == 0 else 'red'
    folium.Marker(
        coords[idx],
        popup=f"{i+1}: {names[idx]}",
        icon=folium.Icon(color=color)
    ).add_to(m)

folium.PolyLine(
    [coords[i] for i in best_route] + [coords[best_route[0]]],
    color="blue",
    weight=4
).add_to(m)

filename = f"tsp_{NUM_CITIES}_cities.html"
m.save(filename)
webbrowser.open("file://" + os.path.realpath(filename))
