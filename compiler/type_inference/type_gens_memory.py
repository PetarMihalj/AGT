from typing import List

from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts
from .recursive_logger import LogTypes

from ..semantics_parsing import semantic_ast as sa

from .type_gens import func_methods, struct_methods
@add_method_to_list(func_methods)
def gen_heap_alloc_array(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "heap_alloc_array": return False
    if len(argument_types)!=1: return False

    if len(type_argument_types) != 1: return False

    if argument_types[0] != ts.IntType(32): return False

    type_alloc = type_argument_types[0]
    type_size = argument_types[0]
    alloc_dummy_name = tc.scope_man.new_func_name("heap alloc array dummy")

    f = sa.FunctionDefinition(
        "heap_alloc_array",
        ['type_alloc'],
        ['type_size'],
        sa.TypePtrExpression(sa.TypeIdExpression("type_alloc")),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("type_alloc"), 
                    "__eq__",
                    sa.TypeTypeExpression(type_alloc)
                )]
            )),
            sa.TypeDeclarationStatementFunction("_2", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("type_size"), 
                    "__eq__",
                    sa.TypeTypeExpression(type_size)
                )]
            )),
            sa.ReturnStatement(sa.PrimitiveCallExpression(
                alloc_dummy_name, 
                [sa.IdExpression("type_size")],
                ts.PointerType(type_alloc)
            )),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)

    tc.primitives[alloc_dummy_name] = prim.HeapAllocPrimitive(
        type_argument_types[0].mangled_name,
        ts.IntType(32).mangled_name
    )
    return True

@add_method_to_list(func_methods)
def gen_heap_alloc(tc, name: str,
                     type_argument_types: List[Type],
                     argument_types: List[Type],
            ):
    if name != "heap_alloc": return False
    if len(type_argument_types) != 1: return False

    type_alloc = type_argument_types[0]
    alloc_dummy_name = tc.scope_man.new_func_name("heap alloc dummy")

    checks = [
            sa.TypeDeclarationStatementFunction(f"_{i}", sa.TypeAngleExpression("enable_if",
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression(f"_pos_{i}"),
                    "__eq__",
                    sa.TypeTypeExpression(argument_types[i])
                )]
            )) for i in range(len(argument_types))
    ]

    f = sa.FunctionDefinition(
        "heap_alloc",
        ['type_alloc'],
        [f'_pos_{i}' for i in range(len(argument_types))],
        sa.TypePtrExpression(sa.TypeIdExpression("type_alloc")),
        [
            sa.TypeDeclarationStatementFunction("_c", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("type_alloc"), 
                    "__eq__",
                    sa.TypeTypeExpression(type_alloc)
                )]
            ))] + checks +
        [
            sa.InitStatement(
                "assigned",
                sa.PrimitiveCallExpression(
                    alloc_dummy_name, 
                    [sa.IntLiteralExpression(1, 32)],
                    ts.PointerType(type_alloc)
                )),
            sa.CallExpression("__init__",[],
                [sa.IdExpression("assigned")]+[
                    sa.IdExpression(f"_pos_{i}") for i in range(len(argument_types))
                ]
            )
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)

    tc.primitives[alloc_dummy_name] = prim.HeapAllocPrimitive(
        type_argument_types[0].mangled_name,
        ts.IntType(32).mangled_name
    )
    return True

@add_method_to_list(func_methods)
def gen_heap_free(tc, name: str,
                     type_argument_types: List[Type],
                     argument_types: List[Type],
            ):
    if name != "heap_free": return False
    if len(argument_types) != 1: return False
    if len(type_argument_types) != 0: return False

    type_free = argument_types[0]
    free_dummy_name = tc.scope_man.new_func_name("heap free dummy")

    f = sa.FunctionDefinition(
        "heap_free",
        [],
        ['free_target'],
        sa.TypePtrExpression(sa.TypeIdExpression("type_alloc")),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("free_target"), 
                    "__eq__",
                    sa.TypeTypeExpression(type_free)
                )]
            )),
            sa.ExpressionStatement(
                sa.PrimitiveCallExpression(
                    free_dummy_name, 
                    [sa.IdExpression("free_target")],
                    ts.voidType()
                ),
            ),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)

    tc.primitives[alloc_dummy_name] = prim.HeapFreePrimitive(
        type_free.mangled_name,
    )
    return True

