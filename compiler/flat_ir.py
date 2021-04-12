from typing import List, Tuple


# Instructions

class FlatStatement:
    pass


class StackAllocate:
    def __init__(self, dest, typename):
        self.dest = dest
        self.typename = typename


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


class BoolConstant:
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value
