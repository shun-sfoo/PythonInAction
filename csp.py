# 很多要用 **计算工具** 来解决的问题基本都可归类为
# 约束满足问题 constraint-satisfaction problem
# CSP 由一组变量构成， 变量可能的取值范围被称为 **值域**
# 要求解 约束满足问题 需要满足变量之间的 **约束**
# 变量 值域 约束
# 编程语言常用技术是构建一个由 **回溯搜索** 和 **几种启发式信息** 组合而成的框架
# 加入启发式是为了提高搜索的性能
# 采用简单的递归回溯搜索法来求解约束满足问题
from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod

V = TypeVar("V")  # variable type
D = TypeVar("D")  # domain type


# Base class for all constraints
class Constraint(Generic[V, D], ABC):
    """
    Docstring for Constraint
    约束将用 Constraint 抽象基类来定义
    variables: 受其约束的变量
    satisfied(): 是否满足条件的方法
    **确认是否满足约束是开始定义某个约束满足问题所需要的主要逻辑**
    """

    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def satisfiled(self, assignment: Dict[V, D]) -> bool: ...


class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        """
        :param self: csp 是变量， 值域和约束的汇集点

        :param variables: 变量的集合
        :type variables: List[V]

        :param domains: 变量映射为可取值的列表 (变量的值域) 变量适用的 值的集合
        :type domains: Dict[V, List[D]]

        constraints: 是把每个变量映射为其所受约束的 list 的 dict 类型
        """
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every varaible should have a domain assinged to it.")

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        """
        Docstring for add_constraint

        :param constraint: 约束类
        :type constraint: Constraint[V, D]
        遍历给定约束涉及的所有变量， 并将其这一约束添加到每个变量的constraints映射中
        """
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Varaible in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, varaible: V, assignment: Dict[V, D]) -> bool:
        """
        Docstring for consistent
        赋值操作，  判断给定的变量配置和所选值域是否满足约束
        :param self: Description
        :param varaible: Description
        :type varaible: V
        :param assignment: Description
        :type assignment: Dict[V, D]
        :return: Description
        :rtype: bool
        """
        for constraint in self.constraints[varaible]:
            if not constraint.satisfiled(assignment):
                return False
        return True

    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        """
        Docstring for backtracking_search
        回溯思路如下： 一旦在搜索中碰到障碍， 就会回到碰到障碍之前最后一次做出判断的已知点
        然后选择其他一条路径。 类似深度优先搜索

        :param self: Description
        :param assignment: 首次调用时为空, 通过递归过程中增加
        :type assignment: Dict[V, D]
        :return: Description
        :rtype: Dict[V, D] | None
        """
        # 递归搜索的基线条件是， 每个变量都能找到满足条件的赋值， 一旦找到就会返回满足条件的解的第一个实例，而不会继续搜索下去
        if len(assignment) == len(self.variables):
            return assignment

        # 为了选出一个新变量来探索其值域， 只需遍历所有变量并找出第一个未赋值的变量
        unassigned: List[V] = [v for v in self.variables if v not in assignment]
        first: V = unassigned[0]

        # 尝试为该变量赋予所有可能的域值
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            if self.consistent(first, local_assignment):  # 类似 successors
                result: Optional[Dict[V, D]] = self.backtracking_search(
                    local_assignment
                )
                if result is not None:
                    return result
        return None
