# main.py (المعدل الجديد حسب طلبك)
import webbrowser
import random
from cities import cities
from nearest_neighbor import NearestNeighborTSP
from map_view import draw_map

city_list = sorted(cities.keys())

print("Available cities in Egypt (20 cities):")
for i, city in enumerate(city_list, 1):
    print(f"{i:2}. {city}")

while True:
    try:
        n = int(input("\nEnter the number of cities where you want to solve the TSP problem (from 5 to 20): "))
        if 5 <= n <= 20:
            break
        else:
            print("Please enter a number between 5 and 20.")
    except ValueError:
        print("Please enter a valid number.")

random.seed(42)
selected_city_names = random.sample(city_list, n)

selected_cities = {city: cities[city] for city in selected_city_names}

start_city = selected_city_names[0]
if "Cairo" in selected_cities:
    start_city = "Cairo"

print(f"\nSelected cities ({n}City):")
print(", ".join(selected_city_names))
print(f"Starting point: {start_city}")

solver = NearestNeighborTSP(selected_cities)
path, cost = solver.solve(start=start_city)

print("\nBest path (Nearest Neighbor + 2-opt):")
print(" -> ".join(path))
print(f"Total cost: {round(cost, 2)} KM")

# رسم الخريطة وفتحها
draw_map(selected_cities, path)
webbrowser.open("tsp_egypt_map.html")