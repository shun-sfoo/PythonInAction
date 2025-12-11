from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random

from math import sqrt
from generic_search import dfs, Node, node_to_path

# from generic_search import dts, bfs, node_to_path， astar, Node


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    row: int
    column: int


class Maze:
    """
    Docstring for Maze
    稀疏度为20%迷宫， 如果某个随机数超过了当前 sparseness 参数给的阈值，就用路障替换空格
    """

    def __init__(
        self,
        rows: int = 10,
        columns: int = 10,
        sparsencess: float = 0.2,
        start: MazeLocation = MazeLocation(0, 0),
        goal: MazeLocation = MazeLocation(9, 9),
    ) -> None:
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        self._grid: List[List[Cell]] = [
            [Cell.EMPTY for _ in range(columns)] for _ in range(rows)
        ]
        self._randomly_fill(rows, columns, sparsencess)
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    def goal_test(self, ml: MazeLocation) -> bool:
        """
        Docstring for goal_test
        判断是否已抵达目标

        :param self: Description
        :param ml: Description
        :type ml: MazeLocation
        :return: Description
        :rtype: bool
        """
        return ml == self.goal

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []
        if (
            ml.row + 1 < self._rows
            and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if (
            ml.column + 1 < self._columns
            and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output


if __name__ == "__main__":
    maze: Maze = Maze()
    print(maze)
    solution1: Optional[Node[MazeLocation]] = dfs(
        maze.start, maze.goal_test, maze.successors
    )
    if solution1 is None:
        print("No solution")
    else:
        path1: List[MazeLocation] = node_to_path(solution1)
        maze.mark(path1)
        print(maze)
        maze.clear(path1)
