from typing import List, Tuple


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


separator = "_$_"


class Label:
    def __init__(self, name):
        self.name: str = name


class Variable:
    def __init__(self, name, type_var_name, type_annotation):
        self.name: str = name
        self.type_var_name: str = type_var_name
        self.type_annotation: str = type_annotation


class VariablePointer:
    def __init__(self, name, type_var_name, type_annotation):
        self.name: str = name
        self.type_var_name: str = type_var_name
        self.type_annotation: str = type_annotation


class ScopeManager:
    def __init__(self):
        self.scope_stack: List[dict[str]] = [None]
        self.label_cnt = 0
        self.tmp_var_cnt = 0
        self.var_cnt = 0

    def begin_scope(self):
        self.scope_stack.append(dict())

    def end_scope(self):
        self.scope_stack.pop()

    def get_var(self, name: str):
        for s in reversed(self.scope_stack):
            if name in s:
                return s[name]

    def new_label(self, description="") -> Label:
        self.label_cnt += 1
        return Label("label " + description + separator + self.label_cnt)

    def new_tmp_var(self, description="") -> Variable:
        self.tmp_var_cnt += 1
        return Variable("tmp_var " + description +
                        separator + self.tmp_var_cnt,
                        "tmp_var_type " + description +
                        separator + self.tmp_var_cnt,
                        None)

    def new_var(self, name, type_annotation=None) -> Variable:
        self.var_cnt += 1
        res_var = "var " + separator + name + separator + self.var_cnt
        res_var_type = "var_type " + separator + name +\
            separator + self.var_cnt
        self.scope_stack[-1][name] = (res_var, res_var_type)
        return Variable(res_var, res_var_type, type_annotation)


class FlatIR:
    def __init__(self):
        self.func_defs: List[FunctionDefinition] = []
        self.struct_defs: List[StructDefinition] = []
        self.type_env: List = []

    def start_func(self, name):
        self.func_defs.append(FunctionDefinition(name))

    def start_struct(self, name):
        self.struct_defs.append(StructDefinition(name))

    def func(self):
        return self.func_defs[-1]

    def struct(self):
        return self.struct_defs[-1]


class FunctionDefinition:
    def __init__(self, name):
        self.name = name
        self.parameters: List[Variable] = []
        self.return_var: str = None
        self.body = []
        self.declarations = []


class StructDefinition:
    def __init__(self, typeName):
        self.typeName: str = typeName
        self.type_parameters = []
        self.members: List[Tuple[str, str]] = []


class Assignment:
    def __init__(self, dest, src):
        self.dest = dest
        self.src = src


class FunctionCallAssignment:
    def __init__(self, dest, fn_name, arguments):
        self.dest: Variable = dest
        self.fn_name: str = fn_name
        self.arguments: List[Variable] = arguments


class Jump:
    def __init__(self, var, label_true, label_false):
        self.var: Variable = var
        self.label_true: Label = label_true
        self.label_false: Label = label_false


if __name__ == '__main__':
    from lexer import Lexer
    from parser import Parser
    from helpers import tree_print
    data = open('prog3.st').read()
    lexer = Lexer()
    lexer.test(data)
    parser = Parser(lexer, debug=True)
    a = parser.parse(data)
    tree_print(a)
    ir = FlatIR()
    sm = ScopeManager()
    a.get_ir(sm, ir)
    tree_print(ir)
