import heapq
from data.cities import tour_cost

def ucs_tsp(dist):
    """Uniform Cost Search for TSP."""
    n = len(dist)
    start = 0
    pq = []  # (cost, current, mask, path)
    heapq.heappush(pq, (0, start, 1 << start, [start]))
    min_cost = float('inf')
    best_tour = None
    visited_states = set()

    while pq:
        cost, curr, mask, path = heapq.heappop(pq)
        if (mask, curr) in visited_states:
            continue
        visited_states.add((mask, curr))

        if len(path) == n:
            total_cost = cost + dist[curr][start]
            if total_cost < min_cost:
                min_cost = total_cost
                best_tour = path + [start]
            continue

        for next_city in range(n):
            if not (mask & (1 << next_city)):
                new_cost = cost + dist[curr][next_city]
                if new_cost >= min_cost:
                    continue  # Prune
                new_mask = mask | (1 << next_city)
                new_path = path + [next_city]
                heapq.heappush(pq, (new_cost, next_city, new_mask, new_path))

    return best_tour, min_cost