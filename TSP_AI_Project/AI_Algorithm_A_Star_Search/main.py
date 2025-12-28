import webbrowser
import time
from cities import group_5, group_15, group_20
from a_star import AStarTSP
from map_view import draw_map

print("=== TSP Solver for Egyptian Cities ===")
print("Choose the group size: 5, 15, or 20 cities (fixed groups, no randomness)\n")

# اختيار عدد المدن
while True:
    try:
        n = int(input("Enter number of cities (5, 15, or 20): "))
        if n in [5, 15, 20]:
            break
        else:
            print("Please enter only 5, 15, or 20.")
    except ValueError:
        print("Please enter a valid number.")

# اختيار الجروب المناسب
if n == 5:
    selected_cities = group_5
    print("\nYou selected: Small Group (5 cities)")
elif n == 15:
    selected_cities = group_15
    print("\nYou selected: Medium Group (15 cities)")
else:
    selected_cities = group_20
    print("\nYou selected: Large Group (20 cities - All cities)")

# عرض المدن المتاحة مرتبة أبجديًا
city_names = sorted(selected_cities.keys())
print("\nAvailable cities in this group:")
for i, city in enumerate(city_names, 1):
    print(f"  {i:2}. {city}")

# اختيار نقطة البداية تلقائيًا
default_start = "Cairo" if "Cairo" in selected_cities else city_names[0]
print(f"\nSolving optimal TSP tour starting and ending at {default_start}...")

# قياس وقت البداية
start_time = time.time()

# تشغيل A* Search
solver = AStarTSP(selected_cities)
path, cost = solver.solve(default_start)

# قياس وقت النهاية
end_time = time.time()
execution_time = end_time - start_time

# عرض النتيجة
print("\n" + "="*60)
print("Best optimal path found (A* Search with MST heuristic):")
print(" → ".join(path))
print(f"Total distance: {round(cost, 2)} km")
print(f"Execution time: {execution_time:.4f} seconds")
print("="*60)

draw_map(selected_cities, path, algorithm_name="A* Algorithm")
print("\nMap generated successfully! Opening in browser...")
webbrowser.open("tsp_egypt_map.html")