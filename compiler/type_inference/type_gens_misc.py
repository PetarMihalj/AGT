from typing import List

from . import inference_errors as ierr
from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts

from ..semantics_parsing import semantic_ast as sa

from .type_gens import func_methods, struct_methods

@add_method_to_list(func_methods)
def gen_cast(tc, name: str,
                 type_argument_types: List[Type],
                 argument_types: List[Type],
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
    tc.primitives.append(prim.CastIntBoolPrimitive(
        dname,
        size_target,
        size_source,
    ))

    ft = ts.FunctionTypePrimitive(dname, type_target)
    return ft
