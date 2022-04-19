class Maze:
    """
    Represents a maze object, represented by a 2-d array of types of nodes
    """

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
