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
def gen_cast(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "cast": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()
    if len(type_argument_types) != 1: raise ierr.TypeGenError()

    type_target = type_argument_types[0]
    type_source = argument_types[0]

    allowed = [ts.IntType(size) for size in [8,16,32,64]]+[ts.BoolType()]
    if type_target not in allowed or type_source not in allowed:
        raise ierr.TypeGenError()

    size_target = type_target.size if isinstance(type_target, ts.IntType) else 1
    size_source = type_source.size if isinstance(type_source, ts.IntType) else 1

    dname = tc.scope_man.new_func_name(f"dummy_cast_{size_source}_to_{size_target}")
    tc.code_blocks.append(prim.CastIntBoolPrimitive(
        dname,
        size_target,
        size_source,
    ))

    ft = ts.FunctionType(
        dname, 
        type_target,
        do_not_copy_args = False,
    )
    return ft
