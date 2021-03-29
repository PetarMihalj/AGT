from Typing import *


def without_nxt(node):
    keys = vars(node).keys()
    for k in keys:
        if k != "nxt":
            return getattr(node, k)


def flatten_lists(ast):
    if not hasattr(ast, "__dict__"):
        return
    for k, v in vars(ast).items():
        if hasattr(v, "nxt"):
            nl = [without_nxt(v)]
            while v.nxt is not None:
                v = v.nxt
                nl.append(without_nxt(v))
            setattr(ast, k, list(filter(None, nl)))
            for i in getattr(ast, k):
                flatten_lists(i)
        else:
            flatten_lists(v)


class ScopeManager:
    separator = "_$_"
    def __init__(self):
        self.scope_stack: List[dict[str]] = [None]
        self.scope_tmp_var_ctr: List[int] = [None]
        self.scope_members: List[int] = [0]
        self.func_label_cnt = 0

    def begin_scope(self):
        self.scope_members[-1]+=1
        self.scope_members.append(0)
        self.scope_tmp_var_ctr.append(0)
        self.scope_stack.append(dict())

    def end_scope(self):
        self.scope_stack.pop()
        self.scope_members.pop()
        self.scope_tmp_var_ctr.pop()

    def _scope_name(self):
        return separator + self.scope_members[-1].join(separator)

    def get_var_name(self, name: str):
        for s in reversed(self.scope_stack):
            if name in s:
                return s[name]

    def new_tmp_var(self) -> str:
        self.scope_tmp_var_ctr[-1]+=1
        return _scope_name + "tmp" + separator + self.scope_tmp_var_ctr[-1]

    def new_tmp_label(self, description = "label") -> str:
        self.func_label_cnt +=1
        return f"{description}_{self.func_label_cnt}"

class FlatIR:
    def __init__(self):
        self.func_defs: List[FunctionDefinition] = []
        self.struct_defs: List[StructDefinition] = []



class FunctionDefinition:
    def __init__(self, name):
        self.name = name
        self.stack_declarations: str = []
        self.type_parameters: List[str] = []
        self.parameters: str = []
        self.body = []

class StructDefinition:
    def __init__(self):
        self.name = None
        self.type_parameters = []
        self.members: List[Tuple[str, str]] = []

class Label:
    def __init__(self):
        self.name: str = None


class FunctionCall:
    def __init__(self):
        self.name: str = None
        self.type_arguments: List[str] = []
        self.arguments: str = []


def flatten_definitions(ast):
    pass


if __name__ == '__main__':
    from lexer import Lexer
    from parser import Parser
    from helpers import tree_print
    data = open('prog1.st').read()
    lexer = Lexer()
    lexer.test(data)
    parser = Parser(lexer, debug=True)
    a = parser.parse(data)
    flatten_lists(a)
    tree_print(a)
