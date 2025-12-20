import heapq

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