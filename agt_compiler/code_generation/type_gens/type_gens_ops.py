from typing import Tuple, List
from dataclasses import dataclass

from .. import inference_errors as ierr
from .. import type_system as ts
from .. import context
from ..code_blocks import Primitive 
from ..type_engine import TypingContext

from . import func_methods, concrete_methods, add_method_to_list

# ---------------------------------------------------------------------

mapping_int_binary = {
        "__eq__": (False, "eq"),
        "__ne__": (False, "ne"),
        '__gt__': (False, "sgt"),
        '__lt__': (False, "slt"),
        '__ge__': (False, "sge"),
        '__le__': (False, "sle"),

        '__add__': (True, "add"),
        '__sub__': (True, "sub"),
        '__mul__': (True, "mul"),
        '__div__': (True, "sdiv"),
        '__mod__': (True, "srem"),
}

@add_method_to_list(func_methods)
def gen_int_type_ops(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name not in mapping_int_binary:
        raise ierr.TypeGenError()
    if len(type_argument_types) != 0:
        raise ierr.TypeGenError()
    if len(argument_types) != 2:
        raise ierr.TypeGenError()

    if not isinstance(argument_types[0], ts.IntType):
        raise ierr.TypeGenError()
    if not isinstance(argument_types[1], ts.IntType):
        raise ierr.TypeGenError()
    if argument_types[0].size != argument_types[1].size:
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"dummy_func_{name}")
    retty = argument_types[0] if mapping_int_binary[name][0] else ts.BoolType()

    tc.code_blocks.append(IntTypeOpPrimitive(
        dname,
        name,
        argument_types[0].size, 
    ))

    ft = ts.FunctionType(
        dname, 
        retty,
        do_not_copy_args = False,
    )
    return ft

@dataclass
class IntTypeOpPrimitive(Primitive):
    mangled_name: str
    op: str
    size: int

    def get_code(self):
        def arithmetic(opname):
            return [
                f"define dso_local i{self.size} @{self.mangled_name}(i{self.size} %0, i{self.size} %1) {{",
                f"\t%3 = {opname} nsw i{self.size} %0, %1",
                f"\tret i{self.size} %3",
                f"}}",
            ]
        def comp(opname):
            return [
                f"define dso_local i1 @{self.mangled_name}(i{self.size} %0, i{self.size} %1) {{",
                f"\t%3 = icmp {opname} i{self.size} %0, %1",
                f"\tret i1 %3",
                f"}}",
            ]


        c,opname = mapping_int_binary[self.op]
        if c:
            return arithmetic(opname)
        else:
            return comp(opname)

# ---------------------------------------------------------------------

mapping_bool_binary = {
    "__and__": "and",
    "__or__": "or",
}

@add_method_to_list(func_methods)
def gen_bool_type_ops(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name not in mapping_bool_binary:
        raise ierr.TypeGenError()
    if len(type_argument_types) != 0:
        raise ierr.TypeGenError()
    if len(argument_types) != 2:
        raise ierr.TypeGenError()

    if not isinstance(argument_types[0], ts.BoolType):
        raise ierr.TypeGenError()
    if not isinstance(argument_types[1], ts.BoolType):
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"dummy_func_{name}")
    tc.code_blocks.append(BoolTypeOpPrimitive(
        dname,
        name,
    ))

    ft = ts.FunctionType(
        dname, 
        ts.BoolType(),
        do_not_copy_args = False,
    )
    return ft


@dataclass
class BoolTypeOpPrimitive(Primitive):
    mangled_name: str
    op: str

    def get_code(self):
        return [
            f"define dso_local i1 @{self.mangled_name}(i1 %0, i1 %1) {{",
            f"\t%3 = {mapping_bool_binary[self.op]} i1 %0, %1",
            f"\tret i1 %3",
            f"}}",
        ]

# ---------------------------------------------------------------------

@add_method_to_list(func_methods)
def gen_bool_type_not(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != '__not__':
        raise ierr.TypeGenError()
    if len(type_argument_types) != 0:
        raise ierr.TypeGenError()
    if len(argument_types) != 1:
        raise ierr.TypeGenError()

    if not isinstance(argument_types[0], ts.BoolType):
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"dummy_func_{name}")
    tc.code_blocks.append(BoolTypeNotPrimitive(
        dname,
    ))

    ft = ts.FunctionType(
        dname, 
        ts.BoolType(),
        do_not_copy_args = False,
    )
    return ft


@dataclass
class BoolTypeNotPrimitive(Primitive):
    mangled_name: str

    def get_code(self):
        return [
            f"define dso_local i1 @{self.mangled_name}(i1 %0) {{",
            f"\t%2 = add i1 1, %0",
            f"\tret i1 %2",
            f"}}",
        ]

# ---------------------------------------------------------------------
