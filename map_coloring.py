from csp import Constraint, CSP
from typing import Dict, List, Optional
from enum import StrEnum


class Place(StrEnum):
    WA = "westeraustralia"
    NT = "Northern Territory"
    SA = "South Australia"
    QL = "Queesland"
    NSW = "New South Wales"
    VI = "Victoria"
    TA = "Tasmania"


class Color(StrEnum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class MapColoringConstraint(Constraint[Place, Color]):
    def __init__(self, place1: Place, place2: Place) -> None:
        super().__init__([place1, place2])
        self.place1: Place = place1
        self.place2: Place = place2

    def satisfiled(self, assignment: Dict[Place, Color]) -> bool:
        if self.place1 not in assignment or self.place2 not in assignment:
            return True

        return assignment[self.place1] != assignment[self.place2]


if __name__ == "__main__":
    variables: List[Place] = [
        Place.WA,
        Place.NT,
        Place.SA,
        Place.QL,
        Place.NSW,
        Place.VI,
        Place.TA,
    ]

    domains: Dict[Place, List[Color]] = {}
    for variable in variables:
        domains[variable] = [Color.RED, Color.GREEN, Color.BLUE]

    csp: CSP[Place, Color] = CSP(variables, domains)
    csp.add_constraint(MapColoringConstraint(Place.WA, Place.NT))
    csp.add_constraint(MapColoringConstraint(Place.WA, Place.SA))
    csp.add_constraint(MapColoringConstraint(Place.SA, Place.NT))
    csp.add_constraint(MapColoringConstraint(Place.QL, Place.NT))
    csp.add_constraint(MapColoringConstraint(Place.QL, Place.SA))
    csp.add_constraint(MapColoringConstraint(Place.QL, Place.NSW))
    csp.add_constraint(MapColoringConstraint(Place.NSW, Place.SA))
    csp.add_constraint(MapColoringConstraint(Place.VI, Place.SA))
    csp.add_constraint(MapColoringConstraint(Place.VI, Place.NSW))
    csp.add_constraint(MapColoringConstraint(Place.VI, Place.TA))

    solution: Optional[Dict[Place, Color]] = csp.backtracking_search()
    if solution is None:
        print("No sulution found !")
    else:
        print(solution)
