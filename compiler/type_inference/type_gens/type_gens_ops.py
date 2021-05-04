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
def gen_int_type_ops(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
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
    tc.code_blocks.append(prim.IntTypeOpPrimitive(
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

@add_method_to_list(func_methods)
def gen_bool_type_ops(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
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
    tc.code_blocks.append(prim.IntTypeOpPrimitive(
        dname,
        name,
        1 
    ))

    ft = ts.FunctionType(
        dname, 
        ts.BoolType(),
        do_not_copy_args = False,
    )
    return ft
