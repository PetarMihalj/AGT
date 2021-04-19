from typing import List, Union, Any

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
                    print(f"{len(indent)} {indent} {i.log}")
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

    def print_logs(self, allowed_types):
        self.level_stack[0].print_logs(allowed_types, indent_init)


