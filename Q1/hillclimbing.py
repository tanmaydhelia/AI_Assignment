import copy

# Define the size of the puzzle (n x n)
n = 3

# Define moves for the empty tile: down, left, up, right
rows = [1, 0, -1, 0]
cols = [0, -1, 0, 1]

# Calculate the number of misplaced tiles
def calculate_costs(state, goal):
    count = 0
    for i in range(n):
        for j in range(n):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                count += 1
    return count

# Generate a new state by swapping the empty tile
def generate_new_state(state, empty_pos, new_empty_pos):
    new_state = copy.deepcopy(state)
    x1, y1 = empty_pos
    x2, y2 = new_empty_pos
    new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
    return new_state

# Check if a position is valid within the puzzle bounds
def is_safe(x, y):
    return 0 <= x < n and 0 <= y < n

# Print the puzzle state
def print_state(state):
    for row in state:
        print(" ".join(str(x) for x in row))
    print()

# Hill Climbing algorithm
def hill_climbing(initial, empty_pos, goal):
    current_state = initial
    current_empty_pos = empty_pos
    current_cost = calculate_costs(current_state, goal)

    steps = [current_state]  # To track the path

    while True:
        neighbors = []
        for i in range(4):  # Generate neighbors for all possible moves
            new_empty_pos = [current_empty_pos[0] + rows[i], current_empty_pos[1] + cols[i]]
            if is_safe(new_empty_pos[0], new_empty_pos[1]):
                new_state = generate_new_state(current_state, current_empty_pos, new_empty_pos)
                cost = calculate_costs(new_state, goal)
                neighbors.append((cost, new_state, new_empty_pos))

        # Select the neighbor with the lowest cost
        neighbors.sort(key=lambda x: x[0])
        best_neighbor = neighbors[0]

        if best_neighbor[0] >= current_cost:  # No improvement
            print("Failure: Stuck in local maxima or plateau!")
            return False

        # Move to the best neighbor
        current_cost = best_neighbor[0]
        current_state = best_neighbor[1]
        current_empty_pos = best_neighbor[2]
        steps.append(current_state)

        # Check if the goal is reached
        if current_cost == 0:
            print("Success: Goal reached!")
            print("Steps taken:")
            for step in steps:
                print_state(step)
            return True

# Main code
initial = [[1, 2, 3],
           [5, 6, 0],
           [7, 8, 4]]

goal = [[1, 2, 3],
        [5, 0, 6],
        [8, 7, 4]]

empty_tile_pos = [1, 2]

hill_climbing(initial, empty_tile_pos, goal)
