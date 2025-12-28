import heapq
import math
import time
import folium
import os
import webbrowser
import random
from folium.plugins import PolyLineTextPath

cities_5 = {
    "Cairo": [30.04, 31.23], "Alexandria": [31.20, 29.91], "Luxor": [25.68, 32.64],
    "Aswan": [24.08, 32.89], "Hurghada": [27.25, 33.81]
}

cities_15 = {
    "Cairo": [30.04, 31.23], "Alexandria": [31.20, 29.91], "Luxor": [25.68, 32.64],
    "Aswan": [24.08, 32.89], "Hurghada": [27.25, 33.81], "Suez": [29.96, 32.54],
    "Port Said": [31.26, 32.30], "Tanta": [30.78, 31.00], "Mansoura": [31.04, 31.37],
    "Ismailia": [30.59, 32.27], "Fayoum": [29.30, 30.84], "Minya": [28.09, 30.75],
    "Asyut": [27.17, 31.18], "Sohag": [26.55, 31.69], "Qena": [26.15, 32.71]
}

cities_20 = {
    "Cairo": [30.04, 31.23], "Alexandria": [31.20, 29.91], "Luxor": [25.68, 32.64],
    "Aswan": [24.08, 32.89], "Hurghada": [27.25, 33.81], "Suez": [29.96, 32.54],
    "Port Said": [31.26, 32.30], "Tanta": [30.78, 31.00], "Mansoura": [31.04, 31.37],
    "Ismailia": [30.59, 32.27], "Fayoum": [29.30, 30.84], "Minya": [28.09, 30.75],
    "Asyut": [27.17, 31.18], "Sohag": [26.55, 31.69], "Qena": [26.15, 32.71],
    "Sharm": [27.91, 34.32], "Matruh": [31.35, 27.23], "Zagazig": [30.58, 31.50],
    "Damietta": [31.41, 31.81], "Damanhur": [31.03, 30.47]
}
def calculate_distance(coord1, coord2):
    R = 6371
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def get_dist_matrix(cities_dict):
    names = list(cities_dict.keys())
    n = len(names)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = calculate_distance(cities_dict[names[i]], cities_dict[names[j]])
    return matrix, names


def ucs_tsp(dist_matrix, start_index):
    n = len(dist_matrix)
    pq = [(0, start_index, 1 << start_index, [start_index])]
    visited = {}

    while pq:
        cost, curr, mask, path = heapq.heappop(pq)

        if (mask, curr) in visited and visited[(mask, curr)] <= cost:
            continue
        visited[(mask, curr)] = cost

        if len(path) == n:
            total_cost = cost + dist_matrix[curr][start_index]
            return path + [start_index], total_cost

        for next_city in range(n):
            if not (mask & (1 << next_city)):
                new_cost = cost + dist_matrix[curr][next_city]
                heapq.heappush(pq, (new_cost, next_city, mask | (1 << next_city), path + [next_city]))
    return None, float('inf')


def draw_map(selected_cities, path_names, algorithm_name="Uniform Cost Search (UCS)"):
    first_city_coords = selected_cities[path_names[0]]
    m = folium.Map(location=first_city_coords, zoom_start=6)

    for i, name in enumerate(path_names[:-1]):
        color = 'green' if i == 0 else 'blue'
        folium.Marker(
            location=selected_cities[name],
            popup=f"{i + 1}: {name}",
            icon=folium.Icon(color=color, icon="info-sign")
        ).add_to(m)

    points = [selected_cities[name] for name in path_names]
    line = folium.PolyLine(points, color="red", weight=4, opacity=0.7).add_to(m)

    PolyLineTextPath(
        line,
        '  ►  ',
        repeat=True,
        offset=7,
        attributes={'fill': 'red', 'font-size': '20'}
    ).add_to(m)

    title_html = f'''
        <div style="position: fixed; 
                    top: 10px; left: 50px; width: 500px; height: 60px; 
                    background-color: white; border:2px solid grey; 
                    z-index:9999; font-size:24px; padding: 15px;
                    border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    font-weight: bold; text-align: center;">
            <b>{algorithm_name}</b>
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))

    file_path = "tsp_ucs_result.html"
    m.save(file_path)
    print(f"\nMap saved to: {file_path}")
    webbrowser.open('file://' + os.path.realpath(file_path))


def main():
    print("=== TSP Solver using Uniform Cost Search (UCS) ===")
    choice = input("Enter the number of cities (5, 15, 20): ")

    if choice == '15':
        selected_cities = cities_15
        print("Note: UCS might take a few seconds for 15 cities...")
    elif choice == '20':
        selected_cities = cities_20
        print("Warning: UCS for 20 cities is extremely heavy on RAM and CPU!")
    else:
        selected_cities = cities_5

    dist_matrix, city_names = get_dist_matrix(selected_cities)
    start_idx = random.randint(0, len(city_names) - 1)

    print(f"Starting City: {city_names[start_idx]}")

    start_time = time.time()
    path_indices, total_dist = ucs_tsp(dist_matrix, start_idx)
    end_time = time.time()

    if path_indices:
        path_names = [city_names[i] for i in path_indices]
        print(f"Best Path: {' ➔ '.join(path_names)}")
        print(f"Total Distance: {total_dist:.2f} KM")
        print(f"Execution Time: {end_time - start_time:.5f} Seconds")

        draw_map(selected_cities, path_names, algorithm_name="Uniform Cost Search (UCS)")
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()