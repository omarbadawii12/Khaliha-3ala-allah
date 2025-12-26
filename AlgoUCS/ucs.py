# ucs.py (ملف الخوارزمية - يحتوي على حساب المسافات والـ UCS)

import math
import heapq

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