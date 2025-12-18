import webbrowser
from cities import cities
from a_star import AStarTSP
from map_view import draw_map

solver = AStarTSP(cities)
path, cost = solver.solve(start="Cairo")

print("Best Path:")
print(" -> ".join(path))
print("Total Cost:", round(cost, 2))

draw_map(cities, path)

webbrowser.open("tsp_egypt_map.html")
