import math

class NearestNeighborTSP:
    def __init__(self, cities):
        self.cities = cities

    @staticmethod
    def dist(a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def solve(self, start="Cairo"):
        # Nearest Neighbor
        path = [start]
        unvisited = set(self.cities.keys()) - {start}
        current = start
        total_cost = 0.0

        while unvisited:
            nearest = min(unvisited, key=lambda city: self.dist(self.cities[current], self.cities[city]))
            total_cost += self.dist(self.cities[current], self.cities[nearest])
            path.append(nearest)
            current = nearest
            unvisited.remove(nearest)

        total_cost += self.dist(self.cities[current], self.cities[start])
        path.append(start)

        improved_path, improved_cost = self.two_opt(path, total_cost)

        return improved_path, improved_cost

    def two_opt(self, path, initial_cost):
        best_path = path[:]
        best_cost = initial_cost
        n = len(path) - 1
        improved = True

        while improved:
            improved = False
            for i in range(1, n - 2):
                for j in range(i + 2, n):
                    old1 = self.dist(self.cities[best_path[i-1]], self.cities[best_path[i]])
                    old2 = self.dist(self.cities[best_path[j]], self.cities[best_path[(j+1) % n]])
                    new1 = self.dist(self.cities[best_path[i-1]], self.cities[best_path[j]])
                    new2 = self.dist(self.cities[best_path[i]], self.cities[best_path[(j+1) % n]])

                    delta = (new1 + new2) - (old1 + old2)
                    if delta < -1e-6:
                        best_path[i:j+1] = best_path[i:j+1][::-1]
                        best_cost += delta
                        improved = True

        return best_path, best_cost