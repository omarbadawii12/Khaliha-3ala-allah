import random
from data.cities import tour_cost


def generate_individual(n):
    """Generate a random tour excluding city 0."""
    individual = list(range(1, n))
    random.shuffle(individual)
    return individual


def generate_initial_population(n, pop_size):
    return [generate_individual(n) for _ in range(pop_size)]


def pmx_crossover(parent1, parent2):
    """Partial Mapped Crossover (PMX) - Stable and common for TSP."""
    size = len(parent1)
    if size <= 1:
        return parent1[:], parent2[:]

    # Choose two random crossover points
    cxpoint1 = random.randint(0, size - 1)
    cxpoint2 = random.randint(0, size - 1)
    if cxpoint1 > cxpoint2:
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    # Initialize children with -1 (placeholder)
    child1 = [-1] * size
    child2 = [-1] * size

    # Copy the middle segment directly
    child1[cxpoint1:cxpoint2 + 1] = parent1[cxpoint1:cxpoint2 + 1]
    child2[cxpoint1:cxpoint2 + 1] = parent2[cxpoint1:cxpoint2 + 1]

    # Create mappings for the segment
    mapping1_to_2 = {parent1[i]: parent2[i] for i in range(cxpoint1, cxpoint2 + 1)}
    mapping2_to_1 = {parent2[i]: parent1[i] for i in range(cxpoint1, cxpoint2 + 1)}

    def resolve_mapping(value, mapping):
        while value in mapping:
            value = mapping[value]
        return value

    # Fill the rest of child1 using parent2
    for i in range(size):
        if child1[i] == -1:
            value = parent2[i]
            child1[i] = resolve_mapping(value, mapping1_to_2)

    # Fill the rest of child2 using parent1
    for i in range(size):
        if child2[i] == -1:
            value = parent1[i]
            child2[i] = resolve_mapping(value, mapping2_to_1)

    return child1, child2


def mutate(individual, mutation_rate=0.1):
    """Swap mutation."""
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual


def ga_tsp(dist, pop_size=100, generations=500, mutation_rate=0.1, elitism=10):
    n = len(dist)
    population = generate_initial_population(n, pop_size)

    for gen in range(generations):
        # Calculate fitness (lower cost = higher fitness)
        costs = [tour_cost([0] + ind + [0], dist) for ind in population]
        fitness_scores = [1 / (cost + 1e-6) for cost in costs]

        # Elitism: keep best individuals
        elite_indices = sorted(range(pop_size), key=lambda i: costs[i])[:elitism]
        new_population = [population[i][:] for i in elite_indices]

        # Generate new individuals
        while len(new_population) < pop_size:
            # Tournament selection (simple and fast)
            parent1_idx = random.choice(elite_indices + list(range(pop_size)))
            parent2_idx = random.choice(elite_indices + list(range(pop_size)))

            child1, child2 = pmx_crossover(population[parent1_idx][:], population[parent2_idx][:])

            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)

            new_population.append(child1)
            if len(new_population) < pop_size:
                new_population.append(child2)

        population = new_population[:pop_size]

    # Get best tour
    best_ind = min(population, key=lambda ind: tour_cost([0] + ind + [0], dist))
    best_tour = [0] + best_ind + [0]
    best_cost = tour_cost(best_tour, dist)
    return best_tour, best_cost