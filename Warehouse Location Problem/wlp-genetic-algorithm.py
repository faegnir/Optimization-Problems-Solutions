import numpy as np


def solve_warehouse_location(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        data.append(list(map(float, line.split())))

    num_depots, num_customers = map(int, data[0])
    depot_capacities = [row[0] for row in data[1:num_depots + 1]]
    depot_setup_costs = [row[1] for row in data[1:num_depots + 1]]
    customer_demands = [int(data[i][0]) for i in range(num_depots, num_depots + num_customers * 2, 2)]
    customer_costs = [data[i][0:num_depots] for i in range(num_depots + 2, num_depots + 1 + num_customers * 2, 2)]

    # Convert data to NumPy arrays
    depot_capacities = np.array(depot_capacities)
    depot_setup_costs = np.array(depot_setup_costs)
    customer_demands = np.array(customer_demands)
    customer_costs = np.array(customer_costs)

    # Genetic Algorithm parameters
    population_size = 100
    num_generations = 100
    mutation_rate = 0.1

    np.random.seed(42)

    # Initialize population randomly
    population = np.random.randint(low=0, high=num_depots, size=(population_size, num_customers))

    for generation in range(num_generations):
        # Evaluate fitness of each individual in the population
        fitness = np.zeros(population_size)
        for i in range(population_size):
            assignment = population[i]
            total_cost = np.sum(customer_costs[np.arange(num_customers), assignment])
            total_cost += np.sum(depot_setup_costs * (np.unique(assignment)[:, np.newaxis] == np.arange(num_depots)))
            fitness[i] = -total_cost

        # Select parents for reproduction (tournament selection)
        parent_indices = np.random.choice(population_size, size=population_size, replace=True)
        parents = population[parent_indices]

        # Perform crossover to create offspring
        offspring = np.empty_like(parents)
        for i in range(0, population_size, 2):
            parent1, parent2 = parents[i], parents[i+1]
            crossover_point = np.random.randint(low=0, high=num_customers)
            offspring[i] = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
            offspring[i+1] = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))

        # Perform mutation on offspring
        for i in range(population_size):
            if np.random.random() < mutation_rate:
                mutation_point = np.random.randint(low=0, high=num_customers)
                offspring[i][mutation_point] = np.random.randint(low=0, high=num_depots)

        # Replace population with offspring
        population = offspring

    # Select the best individual as the solution
    best_assignment = population[np.argmax(fitness)]

    # Calculate total cost
    total_cost = np.sum(customer_costs[np.arange(num_customers), best_assignment])
    total_cost += np.sum(depot_setup_costs * (np.unique(best_assignment)[:, np.newaxis] == np.arange(num_depots)))

    # Prepare output
    output = []
    output.append(f"{total_cost:.3f}")
    output.append(' '.join(str(assignment) for assignment in best_assignment))

    with open(output_file, 'w') as file:
        file.write('\n'.join(output))


files = ["4_0", "16_1", "200_2", "500_3"]
for i in range(4):
    input_file = "./instances/wl_{}".format(files[i])
    output_file = "output{}.txt".format(i)
    solve_warehouse_location(input_file, output_file)
