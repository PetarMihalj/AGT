from typing import List

from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts

from ..semantics_parsing import semantic_ast as sa

from .type_gens import func_methods, struct_methods

@add_method_to_list(func_methods)
def gen_in_int32(tc, name: str,
                 type_argument_types: List[Type],
                 argument_types: List[Type],
            ):
    if name != "in": return False
    if len(argument_types)!=0: return False
    if len(type_argument_types) != 1: return False

    type_arg = type_argument_types[0]
    if type_arg != ts.IntType(32):
        return False

    dummy_name = tc.scope_man.new_func_name("in i32 dummy")

    f = sa.FunctionDefinition(
        "in",
        ['type_arg'],
        [],
        sa.TypeIdExpression("type_arg"),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("type_arg"), 
                    "__eq__",
                    sa.TypeTypeExpression(type_arg)
                )]
            )),
            sa.ReturnStatement(sa.PrimitiveCallExpression(
                dummy_name, 
                [],
                type_arg
            )),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)

    tc.primitives.append(prim.InInt32Primitive(dummy_name))
    return True

@add_method_to_list(func_methods)
def gen_out_i32(tc, name: str,
                 type_argument_types: List[Type],
                 argument_types: List[Type],
            ):
    if name != "out": return False
    if len(argument_types)!=1: return False
    if len(type_argument_types) != 0: return False

    type_arg = argument_types[0]
    if type_arg != ts.IntType(32):
        return False

    dummy_name = tc.scope_man.new_func_name("out i32 dummy")

    f = sa.FunctionDefinition(
        "out",
        [],
        ['type_arg'],
        sa.TypeIdExpression("void"),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("type_arg"), 
                    "__eq__",
                    sa.TypeTypeExpression(type_arg)
                )]
            )),
            sa.ExpressionStatement(sa.PrimitiveCallExpression(
                dummy_name, 
                [sa.IdExpression("type_arg")],
                ts.VoidType()
            )),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)

    tc.primitives.append(prim.OutInt32Primitive(dummy_name))
    return True

