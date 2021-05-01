from typing import List

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
        return False
    if len(type_argument_types) != 0:
        return False
    if len(argument_types) != 2:
        return False

    if not isinstance(argument_types[0], ts.IntType):
        return False
    if not isinstance(argument_types[1], ts.IntType):
        return False
    if argument_types[0].size != argument_types[1].size:
        return False

    dname = tc.scope_man.new_func_name(f"dummy_func_{name}")
    retty = argument_types[0] if name in [
            '__add__','__sub__','__mul__','__div__','__mod__'
        ] else ts.BoolType()
    tc.primitives.append(prim.IntTypeOp(
        dname,
        name,
        argument_types[0].size, 
    ))

    ft = ts.FunctionTypePrimitive(dname, retty)
    tc.function_type_container[(name, tuple(type_argument_types), tuple(argument_types))] = ft

    return True

@add_method_to_list(func_methods)
def gen_bool_type_ops(tc, name: str,
                     type_argument_types: List[Type],
                     argument_types: List[Type],
            ):
    if name not in sa.ops_mapping.values():
        return False
    if len(type_argument_types) != 0:
        return False
    if len(argument_types) != 2:
        return False

    if not isinstance(argument_types[0], ts.BoolType):
        return False
    if not isinstance(argument_types[1], ts.BoolType):
        return False

    dname = tc.scope_man.new_func_name(f"dummy_func_{name}")
    tc.primitives.append(prim.IntTypeOp(
        dname,
        name,
        1 
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.BoolType())
    tc.function_type_container[(name, tuple(type_argument_types), tuple(argument_types))] = ft

    return True
