import hashlib
import math
import os
import pickle
import random
from collections import deque

HOME_DIR = os.path.expanduser("~")
MAZE_SAVE_PATH = os.path.join(HOME_DIR, ".saved_mazes")
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
            neighbors = self.get_neighbors(current[0], current[1], path=False)
            self.grid[current[0]][current[1]] = 0
            if len(neighbors) == 0:
                while not self.route_astar(current, self.end):
                    self.grid[current[0]][current[1]] = 1
                    current = path_stack.popleft()
                neighbors = self.get_neighbors(current[0], current[1], path=False)
                neighbors = [
                    neighbor
                    for neighbor in neighbors
                    if self.route_astar(neighbor, self.end)
                ]
                if len(neighbors) == 0:
                    return
                current = neighbors[0]

            sorted_dist = sorted(neighbors, key=lambda val: distance(val, self.end))
            if self.difficulty == 0:
                threshold = 0.6
            elif self.difficulty == 1:
                threshold = 0.5
            else:
                threshold = 0.4
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
            new_neighbors = self.get_neighbors(current[0], current[1], path=False)
            for neighbor in new_neighbors:
                node_queue.append(neighbor)
            if len(new_neighbors) > 0:
                new_visit = new_neighbors.pop()
                self.grid[current[0]][current[1]] = 0
                self.grid[new_visit[0]][new_visit[1]] = 0

    def save_to_file(self, discard_old=False, filename=None):
        if discard_old and self.name in Maze.saved_mazes:
            # Delete maze with same name
            os.remove(os.path.join(Maze.saved_mazes[self.name]))
            del Maze.saved_mazes[self.name]
        # Adding random data to make the hash
        name_to_hash = (
            f"{self.name}{self.difficulty}{self.dim}{self.start[0] * self.end[1]}"
        )
        hashed = hashlib.md5(name_to_hash.encode())
        if not filename:
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
        if new_dim > self.dim:
            self.end = (new_dim - 1, new_dim - 1)
        else:
            self.end = (min(new_dim - 1, self.end[0]), min(new_dim - 1, self.end[1]))
        self.grid = new_grid
        self.dim = new_dim
        # The start and the end must be open
        self.grid[self.start[0]][self.start[1]] = 0
        self.grid[self.end[0]][self.end[1]] = 0

    def route_astar(
        self,
        src,
        dest,
        search_path=False,
        animate=False,
        nodes=None,
        node_from=None,
        g_score=None,
        f_score=None,
    ):
        src = tuple(src)
        dest = tuple(dest)
        if not nodes:
            nodes = set()
            nodes.add(src)

            node_from = {}

            g_score = {src: 0}

            f_score = {src: distance(src, dest)}

        while len(nodes) > 0:
            current = tuple(sorted(nodes, key=lambda x: f_score[x])[0])
            if current == dest:
                if animate:
                    self.grid[current[0]][current[1]] = 2
                return True

            nodes.remove(current)
            neighbors = set()
            neighbors = self.get_neighbors(current[0], current[1], path=search_path)
            for neighbor in neighbors:
                neighbor = tuple(neighbor)
                route_score = g_score[current] + 1
                if neighbor not in g_score or route_score < g_score[neighbor]:
                    node_from[neighbor] = current
                    g_score[neighbor] = route_score
                    f_score[neighbor] = route_score + distance(neighbor, dest)
                    if neighbor not in nodes:
                        nodes.add(neighbor)
            if animate:
                self.grid[current[0]][current[1]] = 2
                return (nodes, node_from, g_score, f_score)
        return False

    def get_neighbors(self, row, col, path=False):
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
                neighbor = (row + d[0], col + d[1])
                neighbor_value = self.grid[neighbor[0]][neighbor[1]]
                if path:
                    # If all we want is the path neighbors, just check for the ones
                    # that are paths, meaning 0 or 2
                    if neighbor_value == 0 or neighbor_value == 2:
                        neighbors.add(neighbor)
                else:
                    # Otherwise, we are trying to avoid paths
                    # This means that we are also avoiding nodes which neighbor paths
                    # For example, finding neighbors of x where path is false
                    # ...
                    # 0 1 0 1
                    # 0 x 1 1
                    # 1 1 1 1
                    # 1 1 1 1
                    # ...
                    # Here, the node to the direct right is invalid, because
                    # creating a path there would connect to the path in the top right
                    # and as such create unintended paths
                    # The only valid neighbor here is the node directly below the x
                    # To check for this, we need to check if there are path neighbors
                    # of our prospective neighbor i.e. checking neighbors one level down

                    # Fetch neighbors of our neighbor
                    path_neighbors_of_neighbor = self.get_neighbors(
                        neighbor[0], neighbor[1], path=True
                    )
                    # However, it is ok (necessary even) that it borders the current
                    # node we are searching from (the x in the example above)
                    # filter that one out so that it doesn't make the neighbor invalid
                    path_neighbors_of_neighbor = set(
                        filter(
                            lambda node: node != (row, col), path_neighbors_of_neighbor
                        )
                    )
                    # We should have no neighbors that are paths and the node itself
                    # should not be a path as well. If both met, add it.
                    if len(path_neighbors_of_neighbor) == 0 and neighbor_value == 1:
                        neighbors.add(neighbor)
        return neighbors


def distance(a, b):
    return math.sqrt((b[1] - a[1]) ** 2 + (b[0] - a[0]) ** 2)


Maze.load_saved_mazes()
