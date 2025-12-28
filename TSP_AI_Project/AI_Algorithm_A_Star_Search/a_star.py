import math
import heapq

class AStarTSP:
    def __init__(self, cities):
        self.cities = cities
        self.R = 6371.0

    def haversine_distance(self, c1, c2):
        lat1, lon1 = math.radians(c1[0]), math.radians(c1[1])
        lat2, lon2 = math.radians(c2[0]), math.radians(c2[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return self.R * c

    distance = haversine_distance

    def mst_heuristic(self, unvisited):
        if len(unvisited) < 2:
            return 0
        points = [self.cities[city] for city in unvisited]
        min_edges = []
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                min_edges.append((self.distance(points[i], points[j]), i, j))
        min_edges.sort()
        parent = list(range(len(points)))
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        mst_cost = 0
        edges_used = 0
        for dist, u, v in min_edges:
            pu, pv = find(u), find(v)
            if pu != pv:
                parent[pu] = pv
                mst_cost += dist
                edges_used += 1
                if edges_used == len(points) - 1:
                    break
        return mst_cost

    def heuristic(self, current, unvisited):
        if not unvisited:
            return 0
        # أقرب مدينة + MST للباقي
        min_to_next = min(self.distance(self.cities[current], self.cities[c]) for c in unvisited)
        mst_remaining = self.mst_heuristic(unvisited)
        return min_to_next + mst_remaining

    def solve(self, start):
        n = len(self.cities)
        best_cost = float('inf')
        best_path = None

        pq = []
        heapq.heappush(pq, (0 + self.heuristic(start, set(self.cities.keys()) - {start}), 0, start, [start], set(self.cities.keys()) - {start}))

        while pq:
            _, cost_so_far, current, path, unvisited = heapq.heappop(pq)

            if cost_so_far >= best_cost:
                continue  # pruning

            if not unvisited:
                return_cost = cost_so_far + self.distance(self.cities[current], self.cities[start])
                if return_cost < best_cost:
                    best_cost = return_cost
                    best_path = path + [start]
                continue

            for next_city in unvisited:
                new_cost = cost_so_far + self.distance(self.cities[current], self.cities[next_city])
                new_unvisited = unvisited - {next_city}
                h = self.heuristic(next_city, new_unvisited)
                estimated_total = new_cost + h

                if estimated_total >= best_cost:
                    continue  # pruning قوي

                heapq.heappush(pq, (estimated_total, new_cost, next_city, path + [next_city], new_unvisited))

        return best_path, best_cost