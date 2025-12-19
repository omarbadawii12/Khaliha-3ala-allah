from typing import List, Tuple

City = Tuple[float, float]

cities_5 = {
    "Cairo": [30.04, 31.23],
    "Alexandria": [31.20, 29.91],
    "Luxor": [25.68, 32.64],
    "Aswan": [24.08, 32.89],
    "Hurghada": [27.25, 33.81]
}

def get_cities() -> List[City]:
    return [tuple(coords) for coords in cities_5.values()]

def get_city_names() -> List[str]:
    return list(cities_5.keys())
