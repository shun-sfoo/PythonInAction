from typing import List, Optional
from generic_search import bfs, Node, node_to_path

MAX_NUM: int = 3


class MCState:
    """
    Docstring for MCState
    missionaries: 西岸有多少传教士
    cannibals: 西岸有多少食人族
    boat: 独木舟是否在西安
    """

    def __init__(self, missionaries: int, cannibals: int, boat: bool) -> None:
        self.wm: int = missionaries
        self.wc: int = cannibals
        self.em: int = MAX_NUM - self.wm
        self.ec: int = MAX_NUM - self.wc
        self.boat: bool = boat

    def __str__(self) -> str:
        return (
            "On the west bank there are {} missionaries and {} cannibals.\n"
            "On the east bank there are {} missionaries and {} cannibals.\n"
            "The boat is on the {} bank."
        ).format(self.wm, self.wc, self.em, self.ec, ("west" if self.boat else "east"))

    @property
    def is_legal(self) -> bool:
        if self.wm < self.wc and self.wm > 0:
            return False
        if self.em < self.ec and self.em > 0:
            return False
        return True

    def goal_test(self) -> bool:
        return self.is_legal and self.em == MAX_NUM and self.ec == MAX_NUM

    def successors(self) -> List[MCState]:
        """
        Docstring for successors
        从独木舟所有的的河岸出发，
        将尝试加入所有可能的1人或2人的过河组合:
        如果西岸有1个以上的传教士那么就有 2个去东岸 1个去东岸
        如果西岸有1个以上的食人魔那么就有 2个去东岸 1个去东岸
        两个都有1个以上 各去1个
        从东岸过来同理 最多有10种可能性， 然后10种里面筛选出 is_legal的方案
        及 该方案的结果要求岸上食人魔不大于传教士


        :param self: Description
        :return: Description
        :rtype: List[MCState]
        """
        sucs: List[MCState] = []
        if self.boat:  # boat on west bank
            if self.wm > 1:
                # 两名 missionaries 去东岸
                sucs.append(MCState(self.wm - 2, self.wc, not self.boat))
            if self.wm > 0:
                sucs.append(MCState(self.wm - 1, self.wc, not self.boat))
            if self.wc > 1:
                sucs.append(MCState(self.wm, self.wc - 2, not self.boat))
            if self.wc > 0:
                sucs.append(MCState(self.wm, self.wc - 1, not self.boat))
            if (self.wc > 0) and (self.wm > 0):
                sucs.append(MCState(self.wm - 1, self.wc - 1, not self.boat))
        else:  # boat on east bank
            if self.em > 1:
                sucs.append(MCState(self.wm + 2, self.wc, not self.boat))
            if self.em > 0:
                sucs.append(MCState(self.wm + 1, self.wc, not self.boat))
            if self.ec > 1:
                sucs.append(MCState(self.wm, self.wc + 2, not self.boat))
            if self.ec > 0:
                sucs.append(MCState(self.wm, self.wc + 1, not self.boat))
            if self.ec > 0 and self.em > 0:
                sucs.append(MCState(self.wm + 1, self.wc + 1, not self.boat))

        return [x for x in sucs if x.is_legal]


def display_soulution(path: List[MCState]) -> None:
    """
    Docstring for display_soulution

    记录最终状态的同时， 遍历解题步骤中的所有状态
    查看最终状态与当前正在迭代状态之间的差异
    以找出每次渡河的传教士和食人族的人数及其方向
    :param path: Description
    :type path: List[MCState]
    """
    if len(path) == 0:
        return
    old_state: MCState = path[0]
    print(old_state)
    for current_state in path[1:]:
        if current_state.boat:
            print(
                "{} missionaries and {} cannibals moved from the east bank to the west bank\n".format(
                    old_state.em - current_state.em, old_state.ec - current_state.ec
                )
            )
        else:
            print(
                "{} missionaries and {} cannibals moved from the west bank to the east bank\n".format(
                    old_state.wm - current_state.wm, old_state.wc - current_state.wc
                )
            )
        print(current_state)
        old_state = current_state


if __name__ == "__main__":
    start: MCState = MCState(MAX_NUM, MAX_NUM, True)
    solution: Optional[Node[MCState]] = bfs(
        start, MCState.goal_test, MCState.successors
    )
    if solution is None:
        print("No solution found!")
    else:
        path: List[MCState] = node_to_path(solution)
        display_soulution(path)
