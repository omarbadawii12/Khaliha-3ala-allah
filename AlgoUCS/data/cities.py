import math


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
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
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