# main.py (الملف الرئيسي - يحتوي على الرسم والتشغيل)

import time
import folium
import os
import webbrowser
import random
from folium.plugins import PolyLineTextPath
from AlgoUCS.cities import cities_5, cities_15, cities_20
from ucs import get_dist_matrix, ucs_tsp


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
                    top: 10px; left: 50px; width: 400px; height: 60px; 
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