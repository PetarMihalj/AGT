from typing import List

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
    if name != "cast": return False
    if len(argument_types)!=1: return False
    if len(type_argument_types) != 1: return False

    type_target = type_argument_types[0]
    type_source = argument_types[0]

    allowed = [ts.IntType(size) for size in [8,16,32,64]]+[ts.BoolType()]
    if type_target not in allowed or type_source not in allowed:
        return False

    cast_dummy_name = tc.scope_man.new_func_name("cast alloc dummy")

    f = sa.FunctionDefinition(
        "cast",
        ['target'],
        ['source'],
        sa.TypeIdExpression("target"),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("target"), 
                    "__eq__",
                    sa.TypeTypeExpression(type_target)
                )]
            )),
            sa.TypeDeclarationStatementFunction("_2", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("source"), 
                    "__eq__",
                    sa.TypeTypeExpression(type_source)
                )]
            )),
            sa.ReturnStatement(sa.PrimitiveCallExpression(
                cast_dummy_name, 
                [sa.IdExpression("source")],
                type_target
            )),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)

    tc.primitives.append(prim.CastPrimitive(
        cast_dummy_name,
        type_target.mangled_name,
        type_source.mangled_name
    ))
    return True
