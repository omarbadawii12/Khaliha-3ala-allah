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

class CustomNearestNeighborTSP(NearestNeighborTSP):
    def solve(self, start, end=None):
        if end is None:
            end = start

        path = [start]
        unvisited = set(self.cities.keys()) - {start}
        current = start
        total_cost = 0.0

        while unvisited:
            nearest = min(unvisited, key=lambda city: self.dist(self.cities[current], self.cities[city]))
            total_cost += self.dist(self.cities[current], self.cities[nearest])
            path.append(nearest)
            current = nearest
            unvisited.remove(nearest)

        if current != end:
            if end in path[1:-1]:
                path.remove(end)
            total_cost += self.dist(self.cities[current], self.cities[end])
            path.append(end)
            current = end

        if start == end:
            total_cost += self.dist(self.cities[current], self.cities[start])
            path.append(start)

        improved_path, improved_cost = self.two_opt(path, total_cost)

        return improved_path, improved_cost

solver = CustomNearestNeighborTSP(selected_cities)
path, cost = solver.solve(start=start_city, end=end_city if end_city != start_city else None)

print("\nBest path (Nearest Neighbor + 2-opt):")
print(" -> ".join(path))
print(f"Total cost: {round(cost, 2)} km (approximate)")

draw_map(selected_cities, path)
webbrowser.open("tsp_egypt_map.html")