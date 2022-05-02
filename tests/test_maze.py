from src.Maze import maze


def test_neighbors():
    """
    Tests finding path neighbors for a maze
    In this case, we test an empty maze and verify that the neighbors
    of the top right node are the nodes to the right and down, but not up or left
    """
    test_maze = maze.Maze("", 10, 0)
    assert test_maze.get_neighbors(0, 0, path=True) == {(0, 1), (1, 0)}


def test_path_neighbors():
    """
    Tests finding valid neighbors while pathfinding to avoid paths
    and nodes next to paths as well
    """
    test_maze = maze.Maze("", 10, 0)
    test_maze.grid = [[1 for _ in range(test_maze.dim)] for _ in range(test_maze.dim)]
    test_maze.grid[0][0] = 0
    test_maze.grid[1][0] = 0
    assert test_maze.get_neighbors(1, 1, path=False) == {
        (1, 2),
        (2, 1),
    }


def test_astar_path():
    """
    Testing a simple case of pathfinding on a small maze
    """
    test_maze = maze.Maze("", 5, 0)
    test_maze.grid = [
        [0, 1, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
    ]
    # We cannot get from (0,0) to anywhere
    assert not test_maze.route_astar((0, 0), (4, 4), search_path=True)
    # We can get from (3, 0) to (4, 4)
    assert test_maze.route_astar((3, 0), (4, 4), search_path=True)


def test_astar_non_path():
    """
    Tests astar in the case where we avoid current path
    """
    test_maze = maze.Maze("", 5, 0)
    test_maze.grid = [
        [0, 0, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1],
    ]
    # With the given parameters, we can complete the path from (3, 1) to the end
    assert test_maze.route_astar((3, 2), (4, 4), search_path=False)
    test_maze.grid = [
        [0, 0, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1],
    ]
    # Now, we have made a bad decision and no longer can get from the end of the path
    # (1, 3) to the end
    assert not test_maze.route_astar((3, 1), (4, 4), search_path=False)


def test_randomize():
    """
    We can't test every possible randomization, but we can try it
    a few times to generally see if it seems reasonably functional
    """
    test_maze = maze.Maze("", 20, 0)
    # Verify we can randomize and solve 50 mazes of a medium size
    # This test takes a few seconds to run
    for _ in range(50):
        test_maze.randomize()
        # Cycle through difficulties
        test_maze.difficulty += 1
        test_maze.difficulty %= 3
        assert test_maze.route_astar(test_maze.start, test_maze.end, search_path=True)
