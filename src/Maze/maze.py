import hashlib
import os
import pickle

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


Maze.load_saved_mazes()
