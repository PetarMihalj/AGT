from typing import List, Tuple
from dataclasses import dataclass
from .type_system import FunctionType

class FlatStatement:
    pass

@dataclass
class StackAllocate:
    dest: str 

    def get_code(self, f: FunctionType):
        return [
            f"\t%{self.dest} = alloca %{f.types[self.dest].mangled_name}",
        ]

@dataclass
class MemoryCopy:
    dest: str
    src: str

    def get_code(self, f: FunctionType):
        #TODO
        tmp = f.new_tmp()
        return [
            f"\t%{tmp} = load %{f.types[self.dest].mangled_name}, %{f.types[self.src].mangled_name}* %{self.src}",
            f"\tstore %{f.types[self.dest].mangled_name} %{tmp}, %{f.types[self.dest].mangled_name}* %{self.dest}",

        ]

@dataclass
class MemoryCopySrcValue:
    dest: str
    src: str

    def get_code(self, f: FunctionType):
        return [
            f"\tstore %{f.types[self.src].mangled_name} %{self.src}, %{f.types[self.src].mangled_name}* %{self.dest}",
        ]

# functional

@dataclass 
class Comment:
    comm: str
    def get_code(self, f: FunctionType):
        return [
            f"\t; {self.comm}",

        ]


@dataclass
class Dereference:
    dest: str
    src: str

@dataclass
class AddressOf:
    dest: str
    src: str
    
    def get_code(self, f: FunctionType):
        return [
            f"\tstore %{f.types[self.src].mangled_name}* %{self.src}, %{f.types[self.dest].mangled_name}* %{self.dest}"

        ]

@dataclass
class IntConstantAssignment:
    dest: str
    value: int
    size: int
    def get_code(self, f: FunctionType):
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
    fn_to_call: FunctionType
    arguments_names: List[str]

    def get_code(self, f: FunctionType):
        tmps = [f.new_tmp() for n in self.fn_to_call.parameter_names_ordered]
        derefs = [f"\t%{tmps[i]} = load %{f.types[n].mangled_name}, %{f.types[n].mangled_name}* %{n}" 
                for i,n in enumerate(self.arguments_names)]

        args_str = ", ".join(["%"+
            self.fn_to_call.types[self.fn_to_call.parameter_names_ordered[i]].mangled_name
            +" %"+tmps[i] for i,n in enumerate(self.arguments_names)])

        dest_tmp = f.new_tmp()

        if self.dest is None:
            return[ "\t; function call"] + derefs+[
                f"\tcall void @{self.fn_to_call.mangled_name}({args_str})",
            ] + ["\t; end call" ]
        else:
            return ["\t; function call"] + derefs+[
                f'\t%{dest_tmp} = call %{self.fn_to_call.types["return"].mangled_name} @{self.fn_to_call.mangled_name}({args_str})',
                f'\tstore %{self.fn_to_call.types["return"].mangled_name} %{dest_tmp}, %{self.fn_to_call.types["return"].mangled_name}* %{self.dest}'
            ] +[ "\t; end call" ]


@dataclass
class FunctionReturn:
    def get_code(self, f: FunctionType):
        from .type_system import VoidType
        if f.types["return"] == VoidType():
            return ["\tret void"]
        else:
            tmp = f.new_tmp()
            return [
                f'\t%{tmp} = load %{f.types["return"].mangled_name}, %{f.types["return"].mangled_name}* %{"return"}',
                f'\tret %{f.types["return"].mangled_name} %{tmp}',
            ]

# flow control

@dataclass
class Label:
    name: str
    def get_code(self, f: FunctionType):
        return [
            f"\t{self.name}:",
        ]

@dataclass
class JumpToLabelConditional:
    var_name: str
    label_true: str
    label_false: str
    def get_code(self, f: FunctionType):
        tmp = f.new_tmp()

        return [
            f"\t%{tmp} = load i1, i1* %{self.var_name}",
            f"\tbr i1 %{tmp}, label %{self.label_true}, label %{self.label_false}",
        ]

@dataclass
class JumpToLabel:
    label: str
    def get_code(self, f: FunctionType):
        return [
            f"\tbr label %{self.label}",
        ]

# pointer control

@dataclass
class GetPointerOffset:
    dest: str
    src: str
    offset_src: str

@dataclass
class GetElementPtr:
    dest: str
    src: str
    element_name: str
