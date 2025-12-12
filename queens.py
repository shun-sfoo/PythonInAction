from typing import Dict, List, Optional
from csp import Constraint, CSP


class QueenConstraint(Constraint[int, int]):
    def __init__(self, columns: List[int]) -> None:
        super().__init__(columns)
        self.columns = columns

    def satisfiled(self, assignment: Dict[int, int]) -> bool:
        """
        Docstring for satisfiled

        :param self: Description
        :param assignment: assignment 是已经前n-1次通过的赋值 + 新的待验证赋值
        :type assignment: Dict[int, int]
        :return: Description
        :rtype: bool
        """
        # q1c = queen 1 column , q1r = queen 1 row
        for q1c, q1r in assignment.items():
            # q2c = queen 2 column
            for q2c in range(q1c + 1, len(self.columns) + 1):
                if q2c in assignment:
                    q2r: int = assignment[q2c]
                    if q1r == q2r:
                        return False
                    if abs(q1r - q2r) == abs(q1c - q2c):
                        return False
        return True


if __name__ == "__main__":
    columns: List[int] = [1, 2, 3, 4, 5, 6, 7, 8]
    rows: Dict[int, List[int]] = {}
    for column in columns:
        rows[column] = [1, 2, 3, 4, 5, 6, 7, 8]
    csp: CSP[int, int] = CSP(columns, rows)
    csp.add_constraint(QueenConstraint(columns))
    solution: Optional[Dict[int, int]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print(solution)
