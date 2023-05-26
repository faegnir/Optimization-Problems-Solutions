import numpy as np
import random
import math


def calculate_total_cost(depot_assignments, depot_capacities, depot_setup_costs, customer_costs):
    num_customers = len(depot_assignments)
    total_cost = 0.0

    # Calculate customer costs
    for i in range(num_customers):
        total_cost += customer_costs[i][depot_assignments[i]]

    # Calculate depot setup costs
    covered_depots = set()
    for assignment in depot_assignments:
        covered_depots.add(assignment)

    for depot in covered_depots:
        total_cost += depot_setup_costs[depot]

    return total_cost


def simulate_annealing(num_depots, num_customers, depot_capacities, depot_setup_costs, customer_costs):
    num_iterations = 1000
    initial_temperature = 100.0
    cooling_factor = 0.95

    # Randomly initialize depot assignments
    depot_assignments = [random.randint(0, num_depots - 1) for _ in range(num_customers)]
    current_cost = calculate_total_cost(depot_assignments, depot_capacities, depot_setup_costs, customer_costs)

    # Perform Simulated Annealing
    temperature = initial_temperature
    while temperature > 0.1:
        for _ in range(num_iterations):
            # Generate a neighboring solution
            neighbor_assignments = depot_assignments.copy()
            customer_idx = random.randint(0, num_customers - 1)
            depot_idx = random.randint(0, num_depots - 1)
            neighbor_assignments[customer_idx] = depot_idx

            # Calculate costs
            neighbor_cost = calculate_total_cost(neighbor_assignments, depot_capacities, depot_setup_costs,
                                                 customer_costs)
            cost_diff = neighbor_cost - current_cost

            # Accept or reject the neighboring solution
            if cost_diff < 0 or random.random() < math.exp(-cost_diff / temperature):
                depot_assignments = neighbor_assignments
                current_cost = neighbor_cost

        # Cool down the temperature
        temperature *= cooling_factor

    return depot_assignments, current_cost


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
    customer_costs = np.array(customer_costs)
    
    # Run Simulated Annealing
    depot_assignments, total_cost = simulate_annealing(num_depots, num_customers, depot_capacities,
                                                      depot_setup_costs, customer_costs)

    # Prepare output
    output = []
    output.append(f"{total_cost:.3f}")
    output.append(' '.join(str(assignment) for assignment in depot_assignments))

    with open(output_file, 'w') as file:
        file.write('\n'.join(output))


files = ["4_1","16_1", "200_2", "500_3"]
for i in range(4):
    input_file = "./instances/wl_{}".format(files[i])
    output_file = "output{}.txt".format(i)
    solve_warehouse_location(input_file, output_file)
