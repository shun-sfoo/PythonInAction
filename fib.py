from typing import Dict, Generator
from functools import lru_cache

memo: Dict[int, int] = {0: 0, 1: 1}


def fib1(n: int) -> int:
    return fib1(n - 1) + fib1(n - 2)


def fib2(n: int) -> int:
    if n < 2:
        return n
    return fib2(n - 1) + fib2(n - 2)


def fib3(n: int) -> int:
    if not n in memo:
        memo[n] = fib3(n - 1) + fib3(n - 2)
    return memo[n]


@lru_cache(maxsize=None)
def fib4(n: int) -> int:
    """
    Docstring for fib4
    lru_cache 可以为任意 **函数** 缓存结果
    maxsize = None 表示没有限制缓存多少次结果

    :param n: Description
    :type n: int
    :return: Description
    :rtype: int
    """
    if n < 2:
        return n
    return fib4(n - 2) + fib4(n - 1)


def fib5(n: int) -> int:
    """
    Docstring for fib5
    性能更好， 迭代法
    递归是反向求解， 迭代时正向求解
    **能用递归方式求解的问题， 也能用迭代方式求解**

    :param n: Description
    :type n: int
    :return: Description
    :rtype: int
    """
    if n == 0:
        return n

    last: int = 0
    next: int = 1

    for _ in range(1, n):
        last, next = next, last + next

    return next


def fib6(n: int) -> Generator[int, None, None]:
    """
    Docstring for fib6
    使用 yield 把 fib 转换成生成器

    :param n: Description
    :type n: int
    :return: Description
    :rtype: Generator[int, None, None]
    """
    if n == 0:
        yield 0
    if n > 0:
        yield 1
    last: int = 0
    next: int = 1
    for _ in range(1, n):
        last, next = next, last + next
        yield next


if __name__ == "__main__":
    print(fib3(50))
    print(fib4(50))
    print(fib5(50))
    for i in fib6(50):
        print(i)
