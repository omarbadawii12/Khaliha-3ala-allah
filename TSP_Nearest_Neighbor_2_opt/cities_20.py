from typing import List, Tuple

City = Tuple[float, float]

cities_20 = {
    "Cairo": [30.04, 31.23],
    "Alexandria": [31.20, 29.91],
    "Luxor": [25.68, 32.64],
    "Aswan": [24.08, 32.89],
    "Hurghada": [27.25, 33.81],
    "Suez": [29.96, 32.54],
    "Port Said": [31.26, 32.30],
    "Tanta": [30.78, 31.00],
    "Mansoura": [31.04, 31.37],
    "Ismailia": [30.59, 32.27],
    "Fayoum": [29.30, 30.84],
    "Minya": [28.09, 30.75],
    "Asyut": [27.17, 31.18],
    "Sohag": [26.55, 31.69],
    "Qena": [26.15, 32.71],
    "Sharm": [27.91, 34.32],
    "Matruh": [31.35, 27.23],
    "Zagazig": [30.58, 31.50],
    "Damietta": [31.41, 31.81],
    "Damanhur": [31.03, 30.47]
}
def get_cities() -> List[City]:
    return [tuple(coords) for coords in cities_20.values()]

def get_city_names() -> List[str]:
    return list(cities_20.keys())
