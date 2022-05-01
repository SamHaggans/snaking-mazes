import hashlib
import math
import os
import pickle
import random
from collections import deque

# When the file is loaded, try to make the saved_mazes directory in the home folder
# If this fails, the program doesn't run, so print that an error has occured
HOME_DIR = os.path.expanduser("~")
MAZE_SAVE_PATH = os.path.join(HOME_DIR, ".saved_mazes")
if not os.path.isdir(MAZE_SAVE_PATH):
    try:
        os.mkdir(MAZE_SAVE_PATH)
    except OSError as e:
        print(e)


class Maze:
    """
    Represents a Maze object, represented by a 2-d array of types of nodes
    """

    # Class variable for all saved mazes
    saved_mazes = {}

    @staticmethod
    def load_saved_mazes():
        """
        Static method to load all saved mazes from the stored folder
        """
        files = os.listdir(MAZE_SAVE_PATH)
        for filename in files:
            filename = os.path.join(MAZE_SAVE_PATH, filename)
            with open(filename, "rb") as file:
                read_maze = pickle.load(file)
                Maze.saved_mazes[read_maze.name] = filename

    @staticmethod
    def get_saved_maze(name):
        """
        Static method to return a saved maze of a given name
        @param name: Maze name to fetch
        """
        with open(Maze.saved_mazes[name], "rb") as file:
            read_maze = pickle.load(file)
            return read_maze

    def __init__(self, name, dim, difficulty):
        """
        Initializes a Maze
        @param name: Name of the maze
        @param dim: Dimension of the maze, as a number
        @param difficulty: Difficulty of the maze, as a number
        """
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
        """
        Randomizes a maze, respects difficulty settings to change how it randomizes
        """
        # Set everything to a wall initially
        self.grid = [[1 for _ in range(self.dim)] for _ in range(self.dim)]

        # Begin searching at the start of the maze
        current = self.start
        # Store a stack of our path
        path_stack = deque()
        while current != tuple(self.end):
            # Find non-path valid neighbors
            neighbors = self.get_neighbors(current[0], current[1], path=False)
            self.grid[current[0]][current[1]] = 0
            # If we have no neighbors we can go to, we need to backtrack
            if len(neighbors) == 0:
                # Wait until we get back to some node where we can get to the end
                while not self.route_astar(current, self.end):
                    self.grid[current[0]][current[1]] = 1
                    current = path_stack.popleft()
                neighbors = self.get_neighbors(current[0], current[1], path=False)
                # Find the neighbors we can route to from our backtracking
                neighbors = [
                    neighbor
                    for neighbor in neighbors
                    if self.route_astar(neighbor, self.end)
                ]
                # We *should never* return here, as we should be able to backtrack
                # somewhere with valid neighbors. However, this prevents a crash if
                # somehow something goes terribly wrong
                if len(neighbors) == 0:
                    return
                # Pick a neighbor we can go to and set that as new current
                current = neighbors[0]
            # Sort neighbors by how far away they are from the end
            sorted_dist = sorted(neighbors, key=lambda val: distance(val, self.end))
            # Likelihood of picking the "best" route depends on difficulty
            if self.difficulty == 0:
                threshold = 0.6
            elif self.difficulty == 1:
                threshold = 0.5
            else:
                threshold = 0.4
            rd = random.random()
            # If under threshold, choose the best route
            if rd < threshold or len(sorted_dist) == 1:
                current = sorted_dist[0]
            # otherwise (more in hard difficulties), choose the non-best route
            else:
                current = random.choice(sorted_dist[1:])
            path_stack.appendleft(current)
        # Mark end as a path
        self.grid[self.end[0]][self.end[1]] = 0

        # We now have a single path from start to end
        # Now, we need to generate the additional dead-ends along the path

        # Depth first search
        node_queue = path_stack
        while len(node_queue) != 0:
            # Pick a new node
            current = node_queue.pop()
            # Get neighbors and add all of them as potential new nodes
            new_neighbors = self.get_neighbors(current[0], current[1], path=False)
            for neighbor in new_neighbors:
                node_queue.append(neighbor)
            if len(new_neighbors) > 0:
                # Visit one of the new neighbors
                new_visit = new_neighbors.pop()
                # Mark the source and the new visit as new path
                self.grid[current[0]][current[1]] = 0
                self.grid[new_visit[0]][new_visit[1]] = 0

    def save_to_file(self, discard_old=False, filename=None):
        """
        Saves a maze to a file
        @param discard_old: Discard saved maze with same name, default False
        @param filename: Filename as a string, defaults to maze deciding itself
        """
        # The filename depends on multiple factors for the maze,
        # not just the name. However, when we update a saved maze, we want to update it
        # not make a copy. This means that we have to remove the maze saved with the
        # same name (but potentially different parameters) and then resaveit
        # e.g. if the dimension changes, the resulting hashed name would be different
        # but the maze itself would be the "same" maze, so we want to remove the old
        # file and then save our own
        if discard_old and self.name in Maze.saved_mazes:
            # Delete maze with same name
            os.remove(os.path.join(Maze.saved_mazes[self.name]))
            del Maze.saved_mazes[self.name]

        # Make our own filename if one isn't given
        if not filename:
            # Adding random data to make the hash
            name_to_hash = (
                f"{self.name}{self.difficulty}{self.dim}{self.start[0] * self.end[1]}"
            )
            hashed = hashlib.md5(name_to_hash.encode())
            filename = os.path.join(MAZE_SAVE_PATH, hashed.hexdigest() + ".maze")
        with open(filename, "wb") as file:
            pickle.dump(self, file)
        # Add the filename to the dict of saved mazes
        Maze.saved_mazes[self.name] = filename

    def resize(self, new_dim):
        """
        Resize the maze to a new dimension
        @param new_dim: New dimension for maze
        """
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

    def route_astar(self, src, dest, search_path=False, animate=False, state=None):
        """
        Implements the A* (A Star) search algorithm to route from src to dest in maze
        @param src: Source (x, y)
        @param dest: Destination (x, y)
        @param search_path: Whether to only route through paths or only non-paths
        @param animate: Are we animating (which preserves state and only runs once)
        @param state: State to pass in, normally empty and unused"""
        # Convert src and dest to tuples so that they can be in a set
        src = tuple(src)
        dest = tuple(dest)
        if state:
            # Use passed in state
            nodes = state["nodes"]
            node_from = state["node_from"]
            g_score = state["g_score"]
            f_score = state["f_score"]
            # State may still be empty, in which case initialize as normal
            if len(nodes) == 0:
                nodes.add(src)
                g_score[src] = 0
                f_score[src] = distance(src, dest)
        else:
            # Otherwise, generate base state
            nodes = set()
            nodes.add(src)

            node_from = {}

            g_score = {src: 0}

            f_score = {src: distance(src, dest)}

        # nodes is the list of search nodes we should use
        # node_from tells us what the best path to node goes through
        # which can be used to reconstruct the path at the end
        # g_score tells us the difficulty of getting to a node
        # f_score tells us the difficulty we expect to have getting
        # to dest through node (predicted using distance)

        while len(nodes) > 0:
            # Pick the best current node
            current = tuple(sorted(nodes, key=lambda x: f_score[x])[0])
            if current == dest:
                # At the end, draw the last path and return True
                if animate:
                    self.grid[current[0]][current[1]] = 2
                return True

            # Remove current from the set of nodes we want to check
            nodes.remove(current)
            # Get neighbors of current, either path or non-path
            neighbors = self.get_neighbors(current[0], current[1], path=search_path)
            for neighbor in neighbors:
                neighbor = tuple(neighbor)
                # We moved 1 more distance than what it took to get to current
                route_score = g_score[current] + 1
                if neighbor not in g_score or route_score < g_score[neighbor]:
                    # We have a new best way to get to the neighbor
                    # Update how we get to neighbor and its scores
                    node_from[neighbor] = current
                    g_score[neighbor] = route_score
                    f_score[neighbor] = route_score + distance(neighbor, dest)
                    if neighbor not in nodes:
                        # Add it to the search set
                        nodes.add(neighbor)
            if animate:
                # If we're animating, draw the current node we got to
                # and then return False for not complete yet
                self.grid[current[0]][current[1]] = 2
                return False
        return False

    def get_neighbors(self, row, col, path=False):
        """
        Returns the neighbors of a given node
        @param row: Row of node
        @param col: Column of node
        @param path: Default false, tells us whether to search for only path
        neighbors (true) or only non-path (and non-bordering path) (false)
        """
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
    """
    Distance between two nodes
    @param a: Tuple/List of 2 values representing node 1
    @param b: Tuple/List of 2 values representing node 2
    """
    return math.sqrt((b[1] - a[1]) ** 2 + (b[0] - a[0]) ** 2)


# Load the saved mazes as the file is loaded
Maze.load_saved_mazes()
