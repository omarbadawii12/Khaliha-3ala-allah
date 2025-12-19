import math
import heapq

class AStarTSP:
    def __init__(self, cities):
        self.cities = cities

    @staticmethod
    def distance(a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def heuristic(self, current, unvisited):
        if not unvisited:
            return 0
        return min(self.distance(self.cities[current], self.cities[c]) for c in unvisited)

    def solve(self, start):
        pq = []
        heapq.heappush(pq, (0, start, [start], set(self.cities.keys()) - {start}))

        while pq:
            cost, current, path, unvisited = heapq.heappop(pq)

            if not unvisited:
                return path + [start], cost + self.distance(
                    self.cities[current], self.cities[start]
                )

            for city in unvisited:
                new_cost = cost + self.distance(
                    self.cities[current], self.cities[city]
                )
                h = self.heuristic(city, unvisited - {city})
                heapq.heappush(
                    pq,
                    (new_cost + h, city, path + [city], unvisited - {city})
                )