import time
import urllib.request
import numpy as np
import matplotlib.pyplot as plt

def knapsack_greedy(items, max_weight):
    n_items = len(items)
    # Sort the items by their value-to-weight ratio in decreasing order
    items_sorted = sorted(items, key=lambda x: x[0]/x[1], reverse=True)

    opt_value = 0
    opt_items = [0] * n_items

    # Iterate over the sorted items and add them to the knapsack
    for item in items_sorted:
        weight = item[1]
        value = item[0]
        if max_weight >= weight:
            opt_items[items.index(item)] = 1
            opt_value += value
            max_weight -= weight
    
    return opt_value, opt_items

def knapsack_dynamic_prog(items, max_weight):
    n_items = len(items)
    # Initialize a matrix to store the optimal solution for subproblems
    dp_matrix = np.zeros((n_items+1, max_weight+1), dtype=int)

    for i in range(1, n_items+1):
        for j in range(1, max_weight+1):
            weight = items[i-1][1]
            value = items[i-1][0]
            if weight <= j:
                dp_matrix[i][j] = max(dp_matrix[i-1][j], dp_matrix[i-1][j-weight] + value)
            else:
                dp_matrix[i][j] = dp_matrix[i-1][j]
    
    # Find the items that are included in the optimal solution
    solution = [0] * n_items
    i = n_items
    j = max_weight
    while i > 0 and j > 0:
        if dp_matrix[i][j] != dp_matrix[i-1][j]:
            solution[i-1] = 1
            j -= items[i-1][1]
        i -= 1
    
    return dp_matrix[n_items][max_weight], solution

size_runtime_data = []

# Loop over the data sizes and run the algorithm for each size
for size in [19, 200, 10000]:
    # Read input data from URL
    url = f"https://raw.githubusercontent.com/SamedTemiz/samedtemiz.github.io/main/knapsack/ks_{size}_0"
    with urllib.request.urlopen(url) as f:
        data = f.read().decode('utf-8').split('\n')

    # Parse input data
    n_items, max_weight = map(int, data[0].split())
    items = []
    for line in data[1:]:
        if line:
            item = tuple(map(int, line.split()))
            items.append(item)

    # Run the algorithm and measure the runtime
    start_time = time.time()
    if(size < 300):
        opt_value, opt_items = knapsack_dynamic_prog(items, max_weight)
    else:
        opt_value, opt_items = knapsack_greedy(items, max_weight)
    end_time = time.time()

    # Store the size and runtime data
    size_runtime_data.append((size, end_time - start_time))
    opt_indices = [i+1 for i, item in enumerate(opt_items) if item == 1]
    # Print the optimal value and items
    print(opt_value)
    print(*opt_items)
    print(*opt_indices)



sizes = [x[0] for x in size_runtime_data]
runtimes = [x[1] for x in size_runtime_data]

# Plot the size-runtime graph
plt.plot(sizes, runtimes, 'o-')
plt.xlabel('Size')
plt.ylabel('Runtime (s)')
plt.title('Knapsack Problem')
plt.show()
