from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random

from math import sqrt
from generic_search import dfs, bfs, astar, Node, node_to_path

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


def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    """
    Docstring for euclidean_distance
    欧式距离 两点间最短时直线距离
    采用闭包的形式
    distance 将获取传入的 goal 参数
    每次调用 distance() 都可以引用此变量(持久性)
    这种做法可以创建参数较少的函数

    :param goal: Description
    :type goal: MazeLocation
    :return: Description
    :rtype: Callable[[MazeLocation], float]
    """

    def distance(ml: MazeLocation) -> float:
        xdist: int = ml.column - goal.column
        ydist: int = ml.row - goal.row
        return sqrt((xdist * xdist) + (ydist * ydist))

    return distance


def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    """
    Docstring for manhattan_distance
    曼哈顿距离
    获得两个迷宫位置之间的行数差，并将其与列数差相加

    :param goal: Description
    :type goal: MazeLocation
    :return: Description
    :rtype: Callable[[MazeLocation], float]
    """

    def distance(ml: MazeLocation) -> float:
        xdist: int = abs(ml.column - goal.column)
        ydist: int = abs(ml.row - goal.row)
        return xdist + ydist

    return distance


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

    solution2: Optional[Node[MazeLocation]] = bfs(
        maze.start, maze.goal_test, maze.successors
    )
    if solution2 is None:
        print("No solution")
    else:
        path2: List[MazeLocation] = node_to_path(solution2)
        maze.mark(path2)
        print(maze)
        maze.clear(path2)

    distance = manhattan_distance(maze.goal)
    solution3: Optional[Node[MazeLocation]] = astar(
        maze.start, maze.goal_test, maze.successors, distance
    )
    if solution3 is None:
        print("No solution")
    else:
        path3: List[MazeLocation] = node_to_path(solution3)
        maze.mark(path3)
        print(maze)
        maze.clear(path3)
