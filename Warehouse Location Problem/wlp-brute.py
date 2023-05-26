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

    # Initialize the depot assignments randomly
    depot_assignments = np.random.randint(0, num_depots, size=num_customers)

    # Perform iterations to improve the assignments
    for _ in range(100):
        # Calculate the total cost for the current assignments
        total_cost = 0.0
        for i in range(num_customers):
            total_cost += customer_costs[i][depot_assignments[i]]
        for d in range(num_depots):
            if np.any(depot_assignments == d):
                total_cost += depot_setup_costs[d]

        # Generate a new set of assignments by considering alternatives
        new_assignments = depot_assignments.copy()
        for i in range(num_customers):
            current_assignment = depot_assignments[i]
            alternatives = np.arange(num_depots)
            alternatives = alternatives[alternatives != current_assignment]
            np.random.shuffle(alternatives)

            for alternative in alternatives:
                new_assignments[i] = alternative
                new_total_cost = 0.0
                for j in range(num_customers):
                    new_total_cost += customer_costs[j][new_assignments[j]]
                for d in range(num_depots):
                    if np.any(new_assignments == d):
                        new_total_cost += depot_setup_costs[d]

                if new_total_cost < total_cost:
                    total_cost = new_total_cost
                    depot_assignments[i] = alternative
                    break

    output = []
    output.append(f"{total_cost:.3f}")
    output.append(' '.join(str(assignment) for assignment in depot_assignments))

    with open(output_file, 'w') as file:
        file.write('\n'.join(output))


files = ["4_0", "16_1", "200_2", "500_3"]
for i in range(4):
    input_file = "./instances/wl_{}".format(files[i])
    output_file = "output{}.txt".format(i)
    solve_warehouse_location(input_file, output_file)
