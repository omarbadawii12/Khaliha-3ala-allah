import time

def compare_algorithms(algorithms, cities, dist):
    """Run and compare algorithms."""
    results = {}
    for name, func in algorithms.items():
        start_time = time.time()
        tour, cost = func(dist)
        elapsed = time.time() - start_time
        results[name] = {'tour': tour, 'cost': cost, 'time': elapsed}
    return results