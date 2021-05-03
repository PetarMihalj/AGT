from typing import List

from . import inference_errors as ierr
from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts

from ..semantics_parsing import semantic_ast as sa

from .type_gens import func_methods, struct_methods

@add_method_to_list(func_methods)
def gen_in_intbool(tc, name: str,
                 type_argument_types: List[Type],
                 argument_types: List[Type],
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
    tc.primitives.append(prim.InIntBoolPrimitive(
        dname,
        size
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.IntType(size))
    return ft

@add_method_to_list(func_methods)
def gen_out_intbool(tc, name: str,
                 type_argument_types: List[Type],
                 argument_types: List[Type],
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
    tc.primitives.append(prim.OutIntBoolPrimitive(
        dname,
        size
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.VoidType())
    return ft

