from typing import List, Tuple
from dataclasses import dataclass
from .type_system import FunctionType
from . import type_system as ts

class FlatStatement:
    pass

# operations on stack symbolic registers

@dataclass
class StackAllocate:
    """
    Dest has to be an UNALLOCATED stack symbolic register with a value of type s.
    """
    dest: str 

    def get_code(self, f: FunctionType):
        s = f.types[self.dest].mangled_name
        return [
            f"\t%{self.dest} = alloca %{s}",
        ]

@dataclass
class StackCopy:
    """
    Src has to be a stack symbolic register with a value of type s.
    Dest has to be a stack symbolic register with a value of type s.
    """
    dest: str
    src: str

    def get_code(self, f: FunctionType):
        tmp = f.new_tmp()
        s = f.types[self.dest].mangled_name
        return [
            f"\t%{tmp} = load %{s}, %{s}* %{self.src}",
            f"\tstore %{s} %{tmp}, %{s}* %{self.dest}",
        ]

@dataclass
class StackStore:
    """
    Src has to be a symbolic register with of type s.
    Dest has to be a stack symbolic register with a value of type s.
    """
    dest: str
    src: str

    def get_code(self, f: FunctionType):
        s = f.types[self.src].mangled_name
        return [
            f"\tstore %{s} %{self.src}, %{s}* %{self.dest}",
        ]

'''
same as deref
@dataclass
class StackLoad:
    """
    Src has to be a stack symbolic register with a value of type s.
    Dest becomes a symbolic register of type s.
    """
    dest: str
    src: str

    def get_code(self, f: FunctionType):
        s = f.types[self.src].mangled_name
        return [
            f"\t%{self.dest} = load %{s}, %{s}* %{self.src}",
        ]
'''


# functional


@dataclass
class Dereference:
    """
    Src has to be a stack symbolic register with a value of type PointerType(d).
    Dest has to be a UNALLOCATED stack symbolic register with a value of type d
    """
    dest: str
    src: str

    def get_code(self, f: FunctionType):
        d = f.types[self.dest].mangled_name
        return [
            f"\t%{self.dest} = load %{d}*, %{d}** %{self.src}",
        ]

@dataclass
class AddressOf:
    """
    Src has to be a stack symbolic register with a value of type s.
    Dest has to be a stack symbolic register with a value of type PointerType(s)
    """
    dest: str
    src: str

    def get_code(self, f: FunctionType):
        s = f.types[self.src].mangled_name
        return [
            f"\tstore %{s}* %{self.src}, %{s}** %{self.dest}"
        ]

# pointer control

@dataclass
class GetPointerOffset:
    """
    Src has to be a stack symbolic register with a value of type PointerType(s)
    offset_src has to be a stack symbolic register with a value of IntType(x)
    offset_src_size is an int with value from [8,16,32,64]

    Dest has to be a stack symbolic register with a value of type PointerType(s) 
    """
    dest: str
    src: str
    offset_src: str
    offset_src_size: int

    def get_code(self, f: FunctionType):
        pointer_t = f.types[self.src].mangled_name
        inside_t = f.types[self.src].pointed.mangled_name

        tmp_val = f.new_tmp()
        tmp_ext_val = f.new_tmp()

        tmp_ptr = f.new_tmp()
        tmp_newptr = f.new_tmp()

        return [
            f"%{tmp_val} = load i{offset_src_size}, i{offset_src_size}* %{offset_src}"
            f"%{tmp_ext_val} = sext i{offset_src_size} %{tmp_val} to i64",

            f"%{tmp_ptr} = load %{pointer_t}, %{pointer_t}* %{src}",
            f"%{tmp_newptr} = getelementptr inbounds %{inside_t}, %{pointer_t} %{tmp_ptr}, i64 %{tmp_ext_val}",

            f"store %{pointer_t} %{tmp_newptr}, %{pointer_t}* {dest}",
        ]

@dataclass
class GetElementPtr:
    """
    Src has to be a stack symbolic register with a value of type s

    Dest has to be a UNALLOCATED stack symbolic register with a value of type m same as the type of s.element_name
    """
    dest: str
    src: str
    element_name: str

    def get_code(self, f: FunctionType):
        s = f.types[self.src].mangled_name
        ind = f.types[self.src].members.index(element_name)

        return [
            f"%{dest} = getelementptr inbounds %{s}, %{s}* %{self.src}, i32 0, i32 {ind}"
        ]

@dataclass
class IntConstantAssignment:
    """
    Dest has to be a stack symbolic register with a value of type i{size}.
    """
    dest: str
    value: int
    size: int

    def get_code(self, f: FunctionType):
        return [
            f"\tstore %i{self.size} {self.value}, %i{self.size}* %{self.dest}"
        ]

@dataclass
class BoolConstantAssignment:
    """
    Dest has to be a stack symbolic register with a value of type i{size}.
    """
    dest: str
    value: bool

    def get_code(self, f: FunctionType):
        v = 1 if self.value else 0
        return [
            f"\tstore %i1 {v}, %i1* %{self.dest}"
        ]


@dataclass
class FunctionCall:
    """
    DOES NOT COPY stack symbolic registers!

    dest has to be a stack symbolic register which the result is saved into.
    argument_names should be located in stack symbolic registers [argument_names]
    
    """
    dest: str
    fn_to_call_mn: str
    fn_to_call_retty_mn: str
    arguments_names: List[str]

    def get_code(self, f: FunctionType):
        tmps = [f.new_tmp() for an in self.arguments_names]
        types = [f.types[an].mangled_name for an in self.argument_names]

        derefs = [f"\t%{tmp} = load %{ty}, %{ty}* %{an}" 
            for an,tmp,ty in zip(self.argument_names, self.tmps, self.types)]

        args_str = ", ".join([f"%{ty} %{tmp}" for tmp,ty in zip(tmps,types)])


        if self.dest is None:
            return derefs+[
                f"\tcall void @{self.fn_to_call_mn}({args_str})",
            ]
        else:
            dest_tmp = f.new_tmp()
            return derefs+[
                f'\t%{dest_tmp} = call %{self.fn_to_call_retty_mn} @{self.fn_to_call_mn}({args_str})',
                f'\tstore %{self.fn_to_call_retty_mn} %{dest_tmp}, %{self.fn_to_call_retty_mn}* %{self.dest}'
            ]


@dataclass
class FunctionReturn:
    """
    Exits the function with a value located in a stack symbolic register return or void
    """

    def get_code(self, f: FunctionType):
        from .type_system import VoidType
        if f.types["return"] == VoidType():
            return ["\tret void"]
        else:
            tmp = f.new_tmp()
            ty = f.types["return"].mangled_name
            return [
                f'\t%{tmp} = load %{ty}, %{ty}* %return',
                f'\tret %{ty} %{tmp}',
            ]

# flow control

@dataclass
class Label:
    """
    defines a label
    """
    name: str
    def get_code(self, f: FunctionType):
        return [
            f"\t{self.name}:",
        ]

@dataclass
class JumpToLabelConditional:
    """
    var_name has to be a stack symbolic register with a value of type s = bool.
    label_true and label_false have to be existant label names
    """
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
    """
    label has to be an existant label name
    """
    label: str

    def get_code(self, f: FunctionType):
        return [
            f"\tbr label %{self.label}",
        ]

# misc

@dataclass 
class Comment:
    """
    comm is a nonfunctional string embedded in llvm ir
    """
    comm: str
    def get_code(self, f: FunctionType):
        return [
            f"\t; {self.comm}",
        ]
