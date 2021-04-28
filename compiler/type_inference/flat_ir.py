from typing import List, Tuple


# Instructions

class FlatStatement:
    pass


class StackAllocate:
    def __init__(self, dest, typename):
        self.dest = dest
        self.typename = typename

class MemoryCopy:
    def __init__(self, dest, src):
        self.dest = dest
        self.src = src

class MemoryCopySrcValue:
    def __init__(self, dest, src):
        self.dest = dest
        self.src = src

# functional

class Dereference:
    def __init__(self, dest, src):
        self.dest = dest
        self.src = src

class AddressOf:
    def __init__(self, dest, src):
        self.dest = dest
        self.src = src

class IntConstantAssignment:
    def __init__(self, dest, value, size):
        self.dest = dest
        self.value = value
        self.size = size

class BoolConstantAssignment:
    def __init__(self, dest, value):
        self.dest = dest
        self.value = value

class FunctionCall:
    def __init__(self, dest, fn_mangled_name, arguments):
        self.dest: str = dest
        self.fn_mangled_name = fn_mangled_name
        self.arguments: List[str] = arguments

class FunctionReturn:
    def __init__(self, src):
        self.src = src

# structural

class Label:
    def __init__(self, name):
        self.name = name

class Description:
    def __init__(self, name):
        self.name = name

# flow control

class JumpToLabelTrue:
    def __init__(self, var, label_true):
        self.var: str = var
        self.label_true: str = label_true

class JumpToLabelFalse:
    def __init__(self, var, label_false):
        self.var: str = var
        self.label_false: str = label_false

class JumpToLabel:
    def __init__(self, label):
        self.label: str = label

# pointer control

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



