from typing import TypeVar, Generic, List

T = TypeVar("T")


class Stack(Generic[T]):
    """
    Docstring for Stack
    汉诺塔的移动方式和栈一致 LIFO 后进先出
    """

    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)


def hanoi(begin: Stack[int], end: Stack[int], temp: Stack[int], n: int) -> None:
    """
    Docstring for hanoi
    1. 把上层 n - 1 个圆盘从塔A移到塔B（暂存塔), 用塔C作为中转塔
    2. 把底层圆盘从塔A移到塔C
    3. 把n-1个圆盘从塔B移到塔C, 用塔A中中转塔

    :param begin: Description
    :type begin: Stack[int]
    :param end: Description
    :type end: Stack[int]
    :param temp: Description
    :type temp: Stack[int]
    :param n: Description
    :type n: int
    """
    if n == 1:
        end.push(begin.pop())
    else:
        hanoi(begin, temp, end, n - 1)
        hanoi(begin, end, temp, 1)
        hanoi(temp, end, begin, n - 1)


if __name__ == "__main__":
    num_dics: int = 3
    tower_a: Stack[int] = Stack()
    tower_b: Stack[int] = Stack()
    tower_c: Stack[int] = Stack()
    for i in range(1, num_dics + 1):
        tower_a.push(i)

    hanoi(tower_a, tower_c, tower_b, num_dics)
    print(tower_a)
    print(tower_b)
    print(tower_c)
