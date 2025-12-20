import random, math, folium, webbrowser, os, time

random.seed(42)

def haversine(c1, c2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [c1[0], c1[1], c2[0], c2[1]])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def total_distance(route, coords):
    return sum(haversine(coords[route[i]], coords[route[(i+1)%len(route)]]) for i in range(len(route)))

def hill_climbing(coords):
    n = len(coords)
    current_route = list(range(n))
    random.shuffle(current_route)
    current_cost = total_distance(current_route, coords)
    while True:
        best_neighbor, best_cost = current_route, current_cost
        for i in range(n):
            for j in range(i + 1, n):
                neighbor = current_route[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                cost = total_distance(neighbor, coords)
                if cost < best_cost: best_neighbor, best_cost = neighbor, cost
        if best_cost >= current_cost: break
        current_route, current_cost = best_neighbor, best_cost
    return current_route, current_cost

cities = {"Cairo": [30.04, 31.23], "Alexandria": [31.20, 29.91], "Luxor": [25.68, 32.64], "Aswan": [24.08, 32.89], "Hurghada": [27.25, 33.81]}
names, coords = list(cities.keys()), list(cities.values())
RESTARTS = 20

print(f"--- Running TSP: 5 Cities (Stable) ---")
start_t = time.time()
best_route, best_dist = None, float('inf')
for _ in range(RESTARTS):
    r, c = hill_climbing(coords)
    if c < best_dist: best_route, best_dist = r, c
end_t = time.time()

print("\n" + "="*45 + f"\nExecution Time: {end_t - start_t:.6f} sec\nBest Distance: {best_dist:.2f} km\nPath: {' -> '.join([names[i] for i in best_route])} -> {names[best_route[0]]}\n" + "="*45)

m = folium.Map(location=coords[best_route[0]], zoom_start=6)
for i, idx in enumerate(best_route):
    color = 'green' if i == 0 else 'red'
    folium.Marker(coords[idx], popup=f"{i+1}: {names[idx]}", icon=folium.Icon(color=color)).add_to(m)
folium.PolyLine([coords[i] for i in best_route] + [coords[best_route[0]]], color="blue", weight=4).add_to(m)
fname = "map_5_cities.html"
m.save(fname)

webbrowser.open("file://" + os.path.realpath(fname))
