from typing import List

from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts
from .recursive_logger import LogTypes

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

    op_dummy_name = tc.scope_man.new_func_name(f"dummy name {name}")

    f = sa.FunctionDefinition(
        f"{name}",
        [],
        ["a", "b"],
        sa.TypeIdExpression("a"),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("a"), 
                    "__eq__",
                    sa.TypeTypeExpression(argument_types[0])
                )]
            )),
            sa.TypeDeclarationStatementFunction("_2", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("b"), 
                    "__eq__",
                    sa.TypeTypeExpression(argument_types[1])
                )]
            )),
            sa.ReturnStatement(sa.PrimitiveCallExpression(
                op_dummy_name, 
                [sa.IdExpression("a"), sa.IdExpression("b")],
                argument_types[0],
            )),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)


    tc.primitives.append(prim.IntTypeOp(
        op_dummy_name,
        name,
        argument_types[0].size, 
    ))
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

    op_dummy_name = tc.scope_man.new_func_name(f"dummy name {name}")

    f = sa.FunctionDefinition(
        f"{name}",
        [],
        ["a", "b"],
        sa.TypeIdExpression("a"),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("a"), 
                    "__eq__",
                    sa.TypeTypeExpression(argument_types[0])
                )]
            )),
            sa.TypeDeclarationStatementFunction("_2", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("b"), 
                    "__eq__",
                    sa.TypeTypeExpression(argument_types[1])
                )]
            )),
            sa.ReturnStatement(sa.PrimitiveCallExpression(
                op_dummy_name, 
                [sa.IdExpression("a"), sa.IdExpression("b")],
                argument_types[0],
            )),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)


    tc.primitives.append(prim.IntTypeOp(
        op_dummy_name,
        name,
        1, 
    ))
    return True
