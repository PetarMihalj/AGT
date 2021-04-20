from typing import List, Union, Any
from enum import Enum

indent_init = ""
indent_diff = " -"

class Log:
    def __init__(self, log, type):
        self.log: str = log
        self.logtype: Any = type


class Level:
    def __init__(self):
        self.logs_and_levels: List[Union[Log,Level]] = []

    def print_logs(self, allowed_types, indent):
        for i in self.logs_and_levels:
            if isinstance(i, Log):
                if i.logtype in allowed_types:
                    print(f"{indent} {i.log}")
            else:
                i.print_logs(allowed_types, indent+indent_diff)



class RecursiveLogger:
    def __init__(self):
        self.level_stack: List[Level] = [Level()]


    def go_in(self):
        l = Level()
        self.level_stack[-1].logs_and_levels.append(l)
        self.level_stack.append(l)

    def go_out(self):
        self.level_stack.pop()

    def log(self, log, logtype):
        self.level_stack[-1].logs_and_levels.append(Log(log,logtype))

    def print_logs(self, log_level):
        log_types = []
        if log_level>=1:
            log_types += [
                LogTypes.FUNCTION_RESOLUTION,
                LogTypes.STRUCT_RESOLUTION,
                LogTypes.FUNCTION_DEFINITION,
                LogTypes.STRUCT_DEFINITION,
                LogTypes.FUNCTION_OR_STRUCT_DEFINITION,
            ]
        if log_level>=2:
            log_types += [
                LogTypes.TYPE_MISSMATCH,
                LogTypes.STATEMENT_ERROR,
                LogTypes.RUNTIME_EXPR_ERROR,
            ]
        if log_level>=3:
            log_types += [
                LogTypes.VISITING,
            ]
        self.level_stack[0].print_logs(log_types, indent_init)


class LogTypes(Enum):
    FUNCTION_RESOLUTION = 1
    STRUCT_RESOLUTION = 2

    FUNCTION_DEFINITION = 3
    STRUCT_DEFINITION = 4

    FUNCTION_OR_STRUCT_DEFINITION = 5

    TYPE_MISSMATCH = 6
    STATEMENT_ERROR = 7
    RUNTIME_EXPR_ERROR = 8

    VISITING = 9
