import webbrowser
import random
from cities import cities
from a_star import AStarTSP
from map_view import draw_map

city_list = sorted(cities.keys())

print("Available cities in Egypt (20 cities):")
for i, city in enumerate(city_list, 1):
    print(f"{i:2}. {city}")

while True:
    try:
        n = int(input("\nEnter the number of cities to solve the TSP for (from 5 to 20): "))
        if 5 <= n <= 20:
            break
        else:
            print("Please enter a number between 5 and 20.")
    except ValueError:
        print("Please enter a valid integer.")

random.seed(42)
selected_city_names = random.sample(city_list, n)
selected_cities = {city: cities[city] for city in selected_city_names}

print(f"\nSelected cities ({n} cities):")
print(", ".join(selected_city_names))

while True:
    start_city = input(f"\nEnter the starting city name (must be one of the selected cities): ").strip().title()
    if start_city in selected_cities:
        break
    else:
        print("This city is not in the selected list. Try again.")

while True:
    end_city = input(f"Enter the ending city name (must be one of the selected cities): ").strip().title()
    if end_city in selected_cities:
        break
    else:
        print("This city is not in the selected list. Try again.")

print(f"\nStart: {start_city}")
print(f"End:   {end_city}")

class CustomAStarTSP(AStarTSP):
    def solve(self, start, end=None):
        if end is None or end == start:
            path, cost = super().solve(start)
            total_cost = cost
            return path, total_cost
        else:
            best_path = None
            best_cost = float('inf')

            for temp_start in selected_cities.keys():
                if temp_start == end:
                    continue
                path, closed_cost = super().solve(temp_start)
                # نحذف العودة الأخيرة إلى temp_start
                open_path = path[:-1]
                if open_path[-1] != end:
                    continue

                open_cost = closed_cost - self.distance(self.cities[end], self.cities[temp_start])

                if open_path[0] == start:
                    final_path = open_path
                else:
                    idx = open_path.index(start)
                    final_path = open_path[idx:] + open_path[:idx]

                if open_cost < best_cost:
                    best_cost = open_cost
                    best_path = final_path + [end]

            if best_path is None:
                path, closed_cost = super().solve(start)
                open_cost = closed_cost - self.distance(self.cities[path[-2]], self.cities[start])
                best_path = path[:-1]
                best_cost = open_cost

            return best_path, best_cost

solver = CustomAStarTSP(selected_cities)

if start_city == end_city:
    path, cost = solver.solve(start=start_city)
else:
    path, cost = solver.solve(start=start_city, end=end_city)

print("\nBest path (A* Search Algorithm):")
print(" -> ".join(path))
print(f"Total cost: {round(cost, 2)} km (approximate)")

draw_map(selected_cities, path)
webbrowser.open("tsp_egypt_map.html")