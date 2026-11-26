
import random

# ==========================================
# 1. DISTANCE MATRIX
# ==========================================

# Delivery locations (excluding depot A)
locations = ['B', 'C', 'D', 'E', 'F', 'G']

# Distance between locations in kilometres
distance = {
    'A': {'A': 0, 'B': 4, 'C': 8, 'D': 6, 'E': 7, 'F': 9, 'G': 5},
    'B': {'A': 4, 'B': 0, 'C': 5, 'D': 7, 'E': 3, 'F': 8, 'G': 6},
    'C': {'A': 8, 'B': 5, 'C': 0, 'D': 4, 'E': 6, 'F': 3, 'G': 7},
    'D': {'A': 6, 'B': 7, 'C': 4, 'D': 0, 'E': 5, 'F': 6, 'G': 8},
    'E': {'A': 7, 'B': 3, 'C': 6, 'D': 5, 'E': 0, 'F': 4, 'G': 6},
    'F': {'A': 9, 'B': 8, 'C': 3, 'D': 6, 'E': 4, 'F': 0, 'G': 5},
    'G': {'A': 5, 'B': 6, 'C': 7, 'D': 8, 'E': 6, 'F': 5, 'G': 0}
}


# ==========================================
# 2. GENETIC ALGORITHM PARAMETERS
# ==========================================

random.seed(42)

POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.2
ELITE_SIZE = 2
TOURNAMENT_SIZE = 3


# ==========================================
# 3. VALIDATE DELIVERY ROUTES
# ==========================================

def is_valid_route(route):

    return len(route) == 6 and set(route) == set(locations)


# ==========================================
# 4. CALCULATE TOTAL ROUTE DISTANCE
# ==========================================

def calculate_distance(route):

    # Start and end the journey at depot A
    full_route = ['A'] + route + ['A']

    total = 0

    # Add the distance between every pair of locations
    for i in range(len(full_route) - 1):

        total += distance[full_route[i]][full_route[i + 1]]

    return total


# ==========================================
# 5. CREATE INITIAL POPULATION
# ==========================================

def create_population():

    population = []

    for _ in range(POPULATION_SIZE):

        # Generate a random route without repeating locations
        route = random.sample(locations, len(locations))

        population.append(route)

    return population


# ==========================================
# 6. TOURNAMENT SELECTION
# ==========================================

def selection(population):

    # Randomly select three candidate routes
    contestants = random.sample(population, TOURNAMENT_SIZE)

    # Choose the route with the shortest distance
    best = min(contestants, key=calculate_distance)

    return best.copy()


# ==========================================
# 7. ORDER CROSSOVER (OX)
# ==========================================

def crossover(parent1, parent2):

    size = len(parent1)

    # Randomly choose a section from parent 1
    start, end = sorted(random.sample(range(size), 2))

    child = [None] * size

    # Copy the selected section from parent 1
    child[start:end + 1] = parent1[start:end + 1]

    # Get remaining locations from parent 2
    remaining = [
        gene for gene in parent2 if gene not in child
    ]

    # Fill the empty positions
    index = list(range(end + 1, size)) + list(range(start))

    for i, gene in zip(index, remaining):

        child[i] = gene

    return child


# ==========================================
# 8. SWAP MUTATION
# ==========================================

def mutation(route):

    # Apply mutation based on the mutation rate
    if random.random() < MUTATION_RATE:

        # Randomly choose two positions
        i, j = random.sample(range(len(route)), 2)

        # Swap the two locations
        route[i], route[j] = route[j], route[i]

    return route


# ==========================================
# 9. GENETIC ALGORITHM
# ==========================================

def genetic_algorithm():

    # Generate the initial population
    population = create_population()

    best_route = None
    best_distance = float('inf')

    print("\nINITIAL POPULATION")
    print("Number of routes:", len(population))

    print("All routes valid:",
          all(is_valid_route(route) for route in population))

    print("\nGENERATION PROGRESS")
    print("-" * 50)

    # Repeat the evolutionary process
    for generation in range(GENERATIONS):

        # Calculate and sort routes by total distance
        population.sort(key=calculate_distance)

        # Update the best solution found so far
        if calculate_distance(population[0]) < best_distance:

            best_route = population[0].copy()

            best_distance = calculate_distance(best_route)

        # Preserve the best routes (elitism)
        new_population = [
            route.copy() for route in population[:ELITE_SIZE]
        ]

        # Create new routes using selection, crossover and mutation
        while len(new_population) < POPULATION_SIZE:

            parent1 = selection(population)
            parent2 = selection(population)

            child = crossover(parent1, parent2)

            child = mutation(child)

            # Check that the new route is valid
            if not is_valid_route(child):
                raise ValueError("Invalid delivery route generated!")

            new_population.append(child)

        population = new_population

        # Display progress at generation 1 and every 10 generations
        if generation == 0 or (generation + 1) % 10 == 0:

            full_route = ['A'] + best_route + ['A']

            print(
                f"Generation {generation + 1}: "
                f"best distance = {best_distance} km"
            )

            print("(" + " -> ".join(full_route) + ")")

    # Check the final population
    population.sort(key=calculate_distance)

    if calculate_distance(population[0]) < best_distance:

        best_route = population[0].copy()

        best_distance = calculate_distance(best_route)

    return best_route, best_distance


# ==========================================
# 10. RUN THE EXPERIMENT
# ==========================================

print("=" * 55)
print("GENETIC ALGORITHM - DELIVERY ROUTE OPTIMISATION")
print("=" * 55)

print(
    f"Seed 42 | Population {POPULATION_SIZE} "
    f"| Generations {GENERATIONS}"
)

# Run the Genetic Algorithm
best_route, best_distance = genetic_algorithm()

# Display the final delivery route
full_route = ['A'] + best_route + ['A']

print("\n" + "=" * 55)
print("FINAL RESULTS")
print("=" * 55)

print("Best route found:", " -> ".join(full_route))

print("Total distance:", best_distance, "km")

print("Route is valid:", is_valid_route(best_route))

print("Number of generations:", GENERATIONS)

print("Population size:", POPULATION_SIZE)

print("Random seed: 42")

print("=" * 55)
