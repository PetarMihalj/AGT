from typing import List

from . import inference_errors as ierr
from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts

from ..semantics_parsing import semantic_ast as sa

from .type_gens import func_methods, struct_methods


@add_method_to_list(func_methods)
def gen_int_type_ops(tc, name: str,
                     type_argument_types: List[Type],
                     argument_types: List[Type],
            ):
    if name not in sa.ops_mapping.values():
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
    retty = argument_types[0] if name in [
            '__add__','__sub__','__mul__','__div__','__mod__'
        ] else ts.BoolType()
    tc.primitives.append(prim.IntTypeOpPrimitive(
        dname,
        name,
        argument_types[0].size, 
    ))

    ft = ts.FunctionTypePrimitive(dname, retty)
    return ft

@add_method_to_list(func_methods)
def gen_bool_type_ops(tc, name: str,
                     type_argument_types: List[Type],
                     argument_types: List[Type],
            ):
    if name not in sa.ops_mapping.values():
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
    tc.primitives.append(prim.IntTypeOpPrimitive(
        dname,
        name,
        1 
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.BoolType())
    return ft
