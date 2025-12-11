from typing import (
    TypeVar,
    Iterable,
    Sequence,
    Any,
    Generic,
    List,
    Callable,
    Set,
    Deque,
    # Dict,
    Optional,
    Protocol,
)

# from heapq import heappush, heappop

T = TypeVar("T")


class Stack(Generic[T]):
    """
    Docstring for Stack
    @property 用在方法上，使其变成了只读的属性，使用时不用加()
    """

    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()

    def __repr__(self) -> str:
        return repr(self._container)


def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False


class Node(Generic[T]):
    """
    Docstring for Node
    Node 是对状态的封装
    用于搜索时记录从一种状态到另一种状态的过程
    (或从一个位置到另一个位置)

    cost, heuristic 用于 A* 算法中
    """

    def __init__(
        self,
        state: T,
        parent: Optional[Node[T]],
        cost: float = 0.0,
        heuristic: float = 0.0,
    ) -> None:
        self.state: T = state
        self.parent: Optional[Node[T]] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node[T]) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(
    initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]
) -> Optional[Node[T]]:
    """
    Docstring for dfs
    深度优先搜索
    frontier: 当前要搜索的状态栈
    explored: 已搜索的状态集
    只要在 frontier 内还有状态要访问，dfs就持续检查该状态是否达到目标，
    并且把将要访问的状态添加进frontier中。
    把搜索的状态打上explored 标记使得搜索不会陷入原地循环

    关于返回 node 作为保存全部路径的思考
    代码中并没有显示设置某个 node.parent = current_node
    而是通过 Node(child, current_node) 把当前current_node 作为后继的父节点
    当最终返回返回的那个节点记录了父节点， 所以其父节点那一条链路上的节点都持有引用不会被回收资源
    而后继中其他节点由于没有被设置成父节点， 所以不会持有引用后续后销毁资源
    TODO: 深度思考在C++中会是如何设置节点，定义节点类, 对于资源的管理。

    :param initial: Description
    :type initial: T
    :param goal_test: Description
    :type goal_test: Callable[[T], bool]
    :param successors: Description
    :type successors: Callable[[T], List[T]]
    :return: Description
    :rtype: Node[T] | None
    """
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        if goal_test(current_state):
            return current_node

        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None


def bfs(
    initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]
) -> Optional[Node[T]]:
    """
    Docstring for bfs
    与dts代码一样， 只是底层从 LIFO 的栈 List 实现， 变成了 FIFO队列 Queue实现

    :param initial: Description
    :type initial: T
    :param goal_test: Description
    :type goal_test: Callable[[T], bool]
    :param successors: Description
    :type successors: Callable[[T], List[T]]
    :return: Description
    :rtype: Node[T] | None
    """
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(current_state)
            frontier.push(Node(child, current_node))
    return None


def node_to_path(node: Node[T]) -> List[T]:
    """
    Docstring for node_to_path
    dfs 执行成功， 返回了封装目标状态的Node
    利用parent属性向前遍历， 即可重现有起点到目标点的路径

    :param node: Description
    :type node: Node[T]
    :return: Description
    :rtype: List[T]
    """
    path: List[T] = [node.state]
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    def __eq__(self, value: Any) -> bool: ...
    def __lt__(self: C, other: C) -> bool: ...
    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low = 0
    high = len(sequence) - 1
    while low <= high:
        mid = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False


if __name__ == "__main__":
    print(linear_contains([1, 5, 15, 15, 15, 15, 20], 5))
    print(binary_contains(["a", "d", "e", "f", "z"], "f"))
    print(binary_contains(["john", "mark", "ronald", "sarah"], "sheila"))
