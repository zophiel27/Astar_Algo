class Node:
    def __init__(n, x, y, g, h, parent=None): #constructor
        n.x = x
        n.y = y
        n.g = g  # g(n) = cost from start node to current node 'n'
        n.h = h  # h(n) = heuristic estimate from current node 'n' to goal node
        n.parent = parent  # its parent node

    def f(n):
        return n.g + n.h  # f(n) = g(n) + h(n)

def heuristic(node, goal):
    # using the Manhattan Distance heuristic
    return abs(node.x - goal.x) + abs(node.y - goal.y)

def is_valid_move(cube, x, y):
    return 0 <= x < len(cube) and 0 <= y < len(cube[0]) and cube[x][y] != 1

def get_neighbors(cube, n):
    neighbors = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        new_x, new_y = n.x + dx, n.y + dy
        if is_valid_move(cube, new_x, new_y):
            neighbors.append(Node(new_x, new_y, 0, 0))
    return neighbors

def A_star(cube, start, goal):
    start_node = Node(start.x, start.y, 0, heuristic(Node(start.x, start.y, 0, 0), goal))
    open = [start_node]
    closed = set()

    while open:
        current_node = min(open, key=lambda node: node.f()) # node with the smallest f value in the open list.
        open.remove(current_node)
        closed.add((current_node.x, current_node.y))

        if (current_node.x, current_node.y) == (goal.x, goal.y):
            path = []
            while current_node is not None:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            path.reverse()
            return path

        for neighbor in get_neighbors(cube, current_node):
            if (neighbor.x, neighbor.y) in closed:
                continue
            temp_g = current_node.g + 1
            if cube[neighbor.x][neighbor.y] == 2:  # if the neighbor is a short wall, add extra cost
                temp_g += 10
            if neighbor not in open or temp_g < neighbor.g:
                neighbor.g = temp_g
                neighbor.h = heuristic(neighbor, goal)
                neighbor.parent = current_node
                if neighbor not in open:
                    open.append(neighbor)
    return None

def readFile(filename):
  cube = []
  with open(filename, 'r') as f:
    for line in f:
      row = [int(char) for char in line.strip('\n')] # removing the newlines using strip()
      cube.append(row)
  return cube
  
def print_maze_with_path(maze, path):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) == path[0]:
                print("S", end=" ")
            elif (i, j) == path[-1]:
                print("G", end=" ")
            elif (i, j) in path:
                print("*", end=" ")
            elif maze[i][j] == 0:
                print("0", end=" ")
            elif maze[i][j] == 1:
                print("1", end=" ")
            elif maze[i][j] == 2:
                print("2", end=" ")
        print()

# main
cube = [
    [1, 0, 0, 0, 1, 0, 0],
    [1, 1, 0, 0, 0, 1, 1],
    [0, 1, 0, 1, 2, 0, 0],
    [1, 1, 0, 1, 1, 2, 1],
    [0, 1, 0, 2, 0, 2, 0],
    [0, 1, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0]
]
# 2 represents the short wall that we can jump over
# 1 represents the wall that we cannot pass through
# 0 represents the path that we can walk through

start = Node(0, 2, 0, 0) # initialises the x, y, g, h parameters
goal = Node(6, 0, 0, 0)

path = A_star(cube, start, goal)
if path:
    print_maze_with_path(cube, path)
    print("Shortest path:", path)
else:
    print("No path found.")
    