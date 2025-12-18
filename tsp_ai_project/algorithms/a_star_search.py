import heapq
from data.cities import tour_cost

def a_star_tsp(dist):
    """A* Search for TSP with simple heuristic."""
    n = len(dist)
    start = 0
    pq = []  # (f, cost, current, mask, path)
    heapq.heappush(pq, (0, 0, start, 1 << start, [start]))
    min_cost = float('inf')
    best_tour = None
    visited_states = set()

    def heuristic(curr, mask, dist):
        unvisited = [i for i in range(n) if not (mask & (1 << i))]
        if not unvisited:
            return 0
        # As per proposal: Euclidean distance to nearest unvisited (assuming dist is Euclidean)
        return min(dist[curr][j] for j in unvisited)

    while pq:
        f, cost, curr, mask, path = heapq.heappop(pq)
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
                    continue
                new_mask = mask | (1 << next_city)
                h = heuristic(next_city, new_mask, dist)
                new_f = new_cost + h
                new_path = path + [next_city]
                heapq.heappush(pq, (new_f, new_cost, next_city, new_mask, new_path))

    return best_tour, min_cost