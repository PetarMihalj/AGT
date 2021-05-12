from typing import List, Union, Any
from enum import Enum

indent_init = ""
indent_diff = " -"

class Level:
    def __init__(self):
        self.logs_and_levels: List[Union[str,Level]] = []

    def print_logs(self, indent):
        for i in self.logs_and_levels:
            if isinstance(i, str):
                print(f"{indent} {i}")
            else:
                i.print_logs(indent+indent_diff)

class RecursiveLogger:
    def __init__(self):
        self.level_stack: List[Level] = [Level()]

    def go_in(self):
        l = Level()
        self.level_stack[-1].logs_and_levels.append(l)
        self.level_stack.append(l)

    def go_out(self):
        self.level_stack.pop()

    def log(self, log):
        self.level_stack[-1].logs_and_levels.append(log)

    def print_logs(self):
        self.level_stack[0].print_logs(indent_init)
