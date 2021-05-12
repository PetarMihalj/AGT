from typing import Tuple

from .. import inference_errors as ierr
from .. import primitives as prim
from .. import type_system as ts
from .. import context
from ...semantics_parsing import semantic_ast as sa

from ...helpers import add_method_to_list
from . import func_methods, struct_methods

from ..type_engine import TypingContext

@add_method_to_list(func_methods)
def gen_in_intbool(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "in": raise ierr.TypeGenError()
    if len(argument_types)!=0: raise ierr.TypeGenError()
    if len(type_argument_types) != 1: raise ierr.TypeGenError()

    type_arg = type_argument_types[0]
    if isinstance(type_arg,ts.IntType):
        size = type_arg.size
    elif isinstance(type_arg, ts.BoolType):
        size = 1
    else:
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"in_i{size}_dummy")
    tc.code_blocks.append(prim.InIntBoolPrimitive(
        dname,
        size
    ))

    ft = ts.FunctionType(
        dname, 
        ts.IntType(size),
        do_not_copy_args = False,
    )
    return ft

@add_method_to_list(func_methods)
def gen_out_intbool(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "out": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()
    if len(type_argument_types) != 0: raise ierr.TypeGenError()

    type_arg = argument_types[0]
    if isinstance(type_arg,ts.IntType):
        size = type_arg.size
    elif isinstance(type_arg, ts.BoolType):
        size = 1
    else:
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"out_i{size}_dummy")
    tc.code_blocks.append(prim.OutIntBoolPrimitive(
        dname,
        size
    ))

    ft = ts.FunctionType(
        dname, 
        None,
        do_not_copy_args = False,
    )
    return ft

@add_method_to_list(func_methods)
def gen_out_char(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "out": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()
    if len(type_argument_types) != 0: raise ierr.TypeGenError()

    type_arg = argument_types[0]
    if not isinstance(type_arg,ts.CharType):
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"out_char_dummy")
    tc.code_blocks.append(prim.OutCharPrimitive(
        dname,
    ))

    ft = ts.FunctionType(
        dname, 
        None,
        do_not_copy_args = False,
    )
    return ft

@add_method_to_list(func_methods)
def gen_out_chararray(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "out": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()
    if len(type_argument_types) != 0: raise ierr.TypeGenError()

    type_arg = argument_types[0]
    if not isinstance(type_arg,ts.PointerType) or not isinstance(type_arg.pointed,ts.CharType):
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"out_char_dummy")
    tc.code_blocks.append(prim.OutCharArrayPrimitive(
        dname,
    ))

    ft = ts.FunctionType(
        dname, 
        None,
        do_not_copy_args = False,
    )
    return ft
