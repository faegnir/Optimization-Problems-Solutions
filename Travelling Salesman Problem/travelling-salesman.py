import math

size = 5
with open("input_paths".format(size), "r") as f:
    data = f.readlines()

data = [line.strip() for line in data]
data = [line.split() for line in data]
data = [[float(x), float(y)] for x, y in data]
locations = [[x, y] for x, y in data]

def calculate_cost(path):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distance(path[i], path[i+1])
    total_distance += distance(path[-1], path[0])
    return total_distance

def distance(p1, p2):
    return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def nearest_neighbor(points):
    path = []
    current_point = points[0]
    path.append(current_point)
    points.remove(current_point)
    while points:
        next_point = min(points, key=lambda x: distance(current_point, x))
        path.append(next_point)
        points.remove(next_point)
        current_point = next_point
    return path

path = nearest_neighbor(locations)
cost = calculate_cost(path)
indices_path = [data.index(point) for point in path]
print("Optimal cost: ", cost)
#array_str = ' '.join(str(element) for element in indices_path)
#print(array_str)
print("City indexes for optimal solution: ", indices_path)