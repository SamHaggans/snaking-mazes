import hashlib
import math
import os
import pickle
import random
from collections import deque

abspath = os.path.abspath(__file__)
relpath = os.path.relpath(__file__)

MAZE_SAVE_PATH = os.path.join(abspath.replace(relpath, ""), ".saved_mazes")
if not os.path.isdir(MAZE_SAVE_PATH):
    try:
        os.mkdir(MAZE_SAVE_PATH)
    except OSError as e:
        print(e)


class Maze:
    """
    Represents a maze object, represented by a 2-d array of types of nodes
    """

    saved_mazes = {}

    @staticmethod
    def load_saved_mazes():
        files = os.listdir(MAZE_SAVE_PATH)
        for filename in files:
            filename = os.path.join(MAZE_SAVE_PATH, filename)
            with open(filename, "rb") as file:
                read_maze = pickle.load(file)
                Maze.saved_mazes[read_maze.name] = filename

    @staticmethod
    def get_saved_maze(name):
        with open(Maze.saved_mazes[name], "rb") as file:
            read_maze = pickle.load(file)
            return read_maze

    def __init__(self, name, dim, difficulty):
        # 0 is an path-available node
        # 1 is a blocked node
        # 2 is a current path node

        self.grid = [[0 for _ in range(dim)] for _ in range(dim)]
        self.name = name
        self.difficulty = difficulty
        self.dim = dim
        self.start = (0, 0)
        self.end = (dim - 1, dim - 1)

    def randomize(self):
        # Set everything to a wall
        self.grid = [[1 for _ in range(self.dim)] for _ in range(self.dim)]

        current = self.start
        path_stack = deque()
        while current != tuple(self.end):
            neighbors = self.get_neighbors(current[0], current[1], exclude_path=True)
            self.grid[current[0]][current[1]] = 0
            if len(neighbors) == 0:
                while not self.route_astar(current, self.end):
                    self.grid[current[0]][current[1]] = 1
                    current = path_stack.popleft()
                neighbors = self.get_neighbors(
                    current[0], current[1], exclude_path=True
                )
                neighbors = [
                    neighbor
                    for neighbor in neighbors
                    if self.route_astar(neighbor, self.end)
                ]
                current = neighbors[0]

            sorted_dist = sorted(neighbors, key=lambda val: distance(val, self.end))
            if self.difficulty == 0:
                threshold = 0.7
            elif self.difficulty == 1:
                threshold = 0.5
            else:
                threshold = 0.3
            rd = random.random()
            if rd < threshold or len(sorted_dist) == 1:
                current = sorted_dist[0]
            else:
                current = random.choice(sorted_dist[1:])
            path_stack.appendleft(current)
        self.grid[self.end[0]][self.end[1]] = 0

        # Breadth first additional path nodes
        node_queue = path_stack
        while len(node_queue) != 0:
            current = node_queue.pop()
            new_neighbors = self.get_neighbors(
                current[0], current[1], exclude_path=True
            )
            for neighbor in new_neighbors:
                node_queue.append(neighbor)
            if len(new_neighbors) > 0:
                new_visit = new_neighbors.pop()
                self.grid[current[0]][current[1]] = 0
                self.grid[new_visit[0]][new_visit[1]] = 0

    def save_to_file(self, discard_old=False):
        if discard_old and self.name in Maze.saved_mazes:
            # Delete maze with same name
            os.remove(os.path.join(Maze.saved_mazes[self.name]))
            del Maze.saved_mazes[self.name]
        # Adding random data to make the hash
        name_to_hash = (
            f"{self.name}{self.difficulty}{self.dim}{self.start[0] * self.end[1]}"
        )
        hashed = hashlib.md5(name_to_hash.encode())
        filename = os.path.join(MAZE_SAVE_PATH, hashed.hexdigest() + ".maze")
        with open(filename, "wb") as file:
            pickle.dump(self, file)
        Maze.saved_mazes[self.name] = filename

    def resize(self, new_dim):
        new_grid = [[0 for _ in range(new_dim)] for _ in range(new_dim)]

        for row in range(min(new_dim, self.dim)):
            for col in range(min(new_dim, self.dim)):
                # Copy original values
                new_grid[row][col] = self.grid[row][col]

        # Start and end may now be invalid
        # Move them in if necessary
        self.start = (min(new_dim - 1, self.start[0]), min(new_dim - 1, self.start[1]))
        self.end = (min(new_dim - 1, self.end[0]), min(new_dim - 1, self.end[1]))
        self.grid = new_grid
        self.dim = new_dim
        self.end = (self.dim - 1, self.dim - 1)

    def route_astar(self, src, dest):
        src = tuple(src)
        dest = tuple(dest)
        nodes = set()
        nodes.add(src)

        node_from = {}

        g_score = {src: 0}

        f_score = {src: distance(src, dest)}

        while len(nodes) > 0:
            current = tuple(sorted(nodes, key=lambda x: f_score[x])[0])
            if current == dest:
                return True

            nodes.remove(current)

            for neighbor in self.get_neighbors(
                current[0], current[1], exclude_path=True
            ):
                neighbor = tuple(neighbor)
                route_score = g_score[current] + 1
                if neighbor not in g_score or route_score < g_score[neighbor]:
                    node_from[neighbor] = current
                    g_score[neighbor] = route_score
                    f_score[neighbor] = route_score + distance(neighbor, dest)
                    if neighbor not in nodes:
                        nodes.add(neighbor)
        return False

    def get_neighbors(self, row, col, exclude_path=False):
        neighbors = set()
        # 4 possible movements (no diagonals)
        delta = ((-1, 0), (0, -1), (0, 1), (1, 0))

        for d in delta:
            if (
                row + d[0] < self.dim
                and row + d[0] >= 0
                and col + d[1] < self.dim
                and col + d[1] >= 0
            ):
                neighbors.add((row + d[0], col + d[1]))

        if exclude_path:
            actual_neighbors = set()
            for neighbor in neighbors:
                neighbor_neighbors = self.get_neighbors(neighbor[0], neighbor[1])
                valid_neighbor = True
                for n in neighbor_neighbors:
                    # For the neighbors of our neighbor, is any of it a path?
                    # If so, our path cannot go through it
                    if self.grid[n[0]][n[1]] == 0 and not (row == n[0] and col == n[1]):
                        valid_neighbor = False
                        break
                if valid_neighbor and self.grid[neighbor[0]][neighbor[1]] != 0:
                    actual_neighbors.add(neighbor)
            neighbors = actual_neighbors

        return neighbors


def distance(a, b):
    return math.sqrt((b[1] - a[1]) ** 2 + (b[0] - a[0]) ** 2)


Maze.load_saved_mazes()
