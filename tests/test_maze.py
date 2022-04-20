from src.Maze import maze


def test_neighbors():
    test_maze = maze.Maze("", 10, 0)
    assert test_maze.get_neighbors(0, 0) == {(0, 1), (1, 0)}


def test_path_neighbors():
    test_maze = maze.Maze("", 10, 0)
    test_maze.grid = [[1 for _ in range(test_maze.dim)] for _ in range(test_maze.dim)]
    test_maze.grid[0][0] = 0
    test_maze.grid[1][0] = 0
    assert test_maze.get_neighbors(1, 1, exclude_path=True) == {
        (1, 2),
        (2, 1),
    }
