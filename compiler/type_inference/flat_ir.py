from typing import List, Tuple
from dataclasses import dataclass


class FlatStatement:
    pass

@dataclass
class StackAllocate:
    dest: str 
    type_mangled_name: str

    def get_code(self):
        return [
            f"\t%{self.dest} = alloca {self.type_mangled_name}",
        ]

@dataclass
class MemoryCopy:
    dest: str
    src: str
    type_mangled_name: str

    def get_code(self):
        #TODO
        return [
            f"%{self.dest} = alloca {self.typename}",
        ]

@dataclass
class MemoryCopySrcValue:
    dest: str
    src: str
    type_mangled_name: str

    def get_code(self):
        return [
            f"\tstore %{self.type_mangled_name} %{self.src}, %{self.type_mangled_name}* %{self.dst}",
        ]

# functional

@dataclass
class Dereference:
    dest: str
    src: str

@dataclass
class AddressOf:
    dest: str
    src: str

@dataclass
class IntConstantAssignment:
    dest: str
    value: int
    size: int
    def get_code(self):
        return [
            f"\tstore %i{self.size} {self.value}, %i{self.size}* %{self.dest}"
        ]

@dataclass
class BoolConstantAssignment:
    dest: str
    value: bool

@dataclass
class FunctionCall:
    dest: str
    fn_mangled_name: str
    arguments: List[str]

@dataclass
class FunctionReturn:
    src: str
    tmp: str
    type_mangled_name: str
    def get_code(self):
        if self.src is None:
            return ["\tret void"]

        else:
            return [
                f"\t%{self.tmp} = load %{self.type_mangled_name}, %{self.type_mangled_name}* %{self.src}",
                f"\tret %{self.type_mangled_name} %{self.tmp}",
            ]

# flow control

@dataclass
class Label:
    name: str

@dataclass
class JumpToLabelTrue:
    var_name: str
    label: str

@dataclass
class JumpToLabelFalse:
    var_name: str
    label: str

@dataclass
class JumpToLabel:
    label: str

# pointer control

@dataclass
class GetPointerOffset:
    def __init__(self, dest, src, offset: int):
        self.dest = dest
        self.src = src
        self.offset = offset


@dataclass
class GetElementPtr:
    def __init__(self, dest, src, element_name):
        self.dest = dest
        self.src = src
        self.element_name = element_name



