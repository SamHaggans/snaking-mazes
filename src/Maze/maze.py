class Maze:
    """
    Represents a maze object, represented by a 2-d array of types of nodes
    """

    def __init_(self, name, dim, difficulty):
        # 0 is an path node
        # 1 is a blocked node

        self.grid = [[0 for _ in dim] for _ in dim]
        self.name = name
        self.difficulty = difficulty

    def set_grid(self, x, y, node_type):
        self.grid[x][y] = node_type
