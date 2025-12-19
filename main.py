import time
import folium
import os
import webbrowser
import random
from data.cities import cities_5, cities_15, cities_20, get_dist_matrix
from algorithms.ucs import ucs_tsp
from folium.plugins import PolyLineTextPath


def draw_map(selected_cities, path_names):
    m = folium.Map(location=[26.8, 30.8], zoom_start=6)
    for i, name in enumerate(path_names[:-1]):
        folium.Marker(location=selected_cities[name], popup=name).add_to(m)

    points = [selected_cities[name] for name in path_names]
    line = folium.PolyLine(points, color="red", weight=4).add_to(m)

    PolyLineTextPath(line, '  ►  ', repeat=True, offset=7,
                     attributes={'fill': 'red', 'font-size': '24'}).add_to(m)

    file_path = "tsp_result_map.html"
    m.save(file_path)
    webbrowser.open('file://' + os.path.realpath(file_path))


def main():
    try:
        choice = input("Enter the number of cities (5, 15, 20): ")
        if choice == '5':
            selected_cities = cities_5
        elif choice == '15':
            selected_cities = cities_15
        elif choice == '20':
            selected_cities = cities_20
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
            print(f"Path Cost (distance): {total_dist:.2f} KM")
            print(f"Execution Time: {end_time - start_time:.5f} Seconds")


            draw_map(selected_cities, path_names)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()