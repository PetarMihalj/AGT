from typing import List, Tuple

separator = "_$_"


class ScopeManager:
    def __init__(self):
        self.scope_stack: List[dict[str]] = []
        self.label_cnt = 0
        self.tmp_var_cnt = 0
        self.var_cnt = 0
        self.break_label_stack = []

    def begin_scope(self):
        self.scope_stack.append(dict())

    def end_scope(self):
        self.scope_stack.pop()

    def get_var_name(self, name: str):
        for s in reversed(self.scope_stack):
            if name in s:
                return s[name]

    def new_label_name(self, description=""):
        self.label_cnt += 1
        return f"label{description}{separator}{self.label_cnt}"

    def new_tmp_var_name(self, description=""):
        self.tmp_var_cnt += 1
        return f"tmp_var{description}{separator}{self.tmp_var_cnt}"

    def new_var_name(self, name):
        self.var_cnt += 1
        res_var = f"var{separator}{name}{separator}{self.var_cnt}"
        self.scope_stack[-1][name] = res_var
        return res_var


# Type system instructions

class FunctionDefinition:
    def __init__(self, name):
        self.name = name
        self.parameters: List[str] = []
        self.typeParameters: List[str] = []
        self.body = []


class StructDefinition:
    def __init__(self, typeName):
        self.typeName: str = typeName
        self.typeParameters: List[str] = []
        self.members: List[Tuple[str, str]] = []

# Type system instructions


class FindFunction:
    def __init__(self, dest, fn_name, args, template_args):
        self.fn_name = fn_name
        self.args = args
        self.template_args = template_args


class FindStruct:
    def __init__(self, dest, struct_name, template_args):
        self.struct_name = struct_name
        self.template_args = template_args

# Instructions

class StackAllocate:
    def __init__(self, dest, typename):
        self.dest = dest
        self.typename = typename


# todo heap allocate and free (probably runtime bindings)


class StoreValueToPointer:
    def __init__(self, dest, src):
        self.dest = dest
        self.src = src


class LoadValueFromPointer:
    def __init__(self, dest, src):
        self.dest = dest
        self.src = src


class Assignment:
    def __init__(self, dest, src):
        self.dest = dest
        self.src = src


class FunctionCall:
    def __init__(self, dest, fn_name, arguments, typeArguments):
        self.dest: str = dest
        self.fn_name = fn_name
        self.arguments: List[str] = arguments
        self.typeArguments: List[str] = typeArguments


class FunctionReturn:
    def __init__(self, src):
        self.src = src


class Label:
    def __init__(self, name):
        self.name = name


class Description:
    def __init__(self, name):
        self.name = name


class JumpToLabelTrue:
    def __init__(self, var, label_true):
        self.var: str = var
        self.label_true: str = label_true


class JumpToLabelFalse:
    def __init__(self, var, label_true):
        self.var: str = var
        self.label_true: str = label_true


class JumpToLabel:
    def __init__(self, label):
        self.label: str = label


class GetPointerOffset:
    def __init__(self, dest, src, offset: int):
        self.dest = dest
        self.src = src
        self.offset = offset


class GetElementPtr:
    def __init__(self, dest, src, element_name):
        self.dest = dest
        self.src = src
        self.element_name = element_name


class IntConstant:
    def __init__(self, dest, value, size, signed):
        self.dest = dest
        self.value = value
        self.size = size
        self.signed = signed


class BoolConstant:
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value


if __name__ == '__main__':
    from lexer import Lexer
    from parser import Parser
    from helpers import tree_print
    data = open('prog1.st').read()
    print(data)
    print()
    # lex and parse
    lexer = Lexer()
    lexer.test(data)
    parser = Parser(lexer, debug=True)
    a = parser.parse(data)
    tree_print(a)
    print()
    # resolve scopes
    defs = []
    sm = ScopeManager()
    a.fill_flat_ir(sm, defs)
    tree_print(defs)
