def calculate_pi(n_terms: int) -> float:
    """
    Docstring for calculate_pi
    莱布尼兹公式
    🍕 = 4/1 - 4/3 + 4/5  - 4/7 + 4/9 - 4/11

    :param n_terms: Description
    :type n_terms: int
    :return: Description
    :rtype: float
    """
    numerator: float = 4.0
    denominator: float = 1.0
    operation: float = 1.0
    pi: float = 0.0
    for _ in range(n_terms):
        pi += operation * (numerator / denominator)
        denominator += 2.0
        operation *= -1.0
    return pi


if __name__ == "__main__":
    print(calculate_pi(1000000))
