from typing import List

from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts

from ..semantics_parsing import semantic_ast as sa

from .type_gens import func_methods, struct_methods


@add_method_to_list(func_methods)
def gen_heap_alloc(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "heap_alloc": return False
    if len(argument_types)!=1: return False

    if len(type_argument_types) != 1: return False

    if not isinstance(argument_types[0], ts.IntType): return False

    type_alloc = type_argument_types[0]
    type_size = argument_types[0]

    dname = tc.scope_man.new_func_name(f"dummy_heap_alloc_array")
    tc.primitives.append(prim.HeapAllocPrimitive(
        dname,
        type_alloc.mangled_name,
        type_size.mangled_name,
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.PointerType(type_alloc))
    tc.function_type_container[(name, tuple(type_argument_types), tuple(argument_types))] = ft

    return True

@add_method_to_list(func_methods)
def gen_heap_free(tc, name: str,
                     type_argument_types: List[Type],
                     argument_types: List[Type],
            ):
    if name != "heap_free": return False
    if len(argument_types) != 1: return False
    if len(type_argument_types) != 0: return False

    type_free_ptr = argument_types[0]
    if not isinstance(type_free_ptr, ts.PointerType): return False

    type_free = type_free_ptr.pointed

    dname = tc.scope_man.new_func_name(f"dummy_heap_free")
    tc.primitives.append(prim.HeapFreePrimitive(
        dname,
        type_free.mangled_name,
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.VoidType())
    tc.function_type_container[(name, tuple(type_argument_types), tuple(argument_types))] = ft

    return True

@add_method_to_list(func_methods)
def gen_heap_init(tc, name: str,
                     type_argument_types: List[Type],
                     argument_types: List[Type],
            ):
    if name != "heap_init": return False
    if len(type_argument_types) != 1: return False

    type_for_alloc = type_argument_types[0]

    checks = [
            sa.TypeDeclarationStatementFunction(f"_{i}", sa.TypeAngleExpression("enable_if",
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression(f"_pos_{i}"),
                    "__eq__",
                    sa.TypeTypeExpression(argument_types[i])
                )]
            )) for i in range(len(argument_types))
    ]
    heap_alloc_fn = tc.resolve_function("heap_alloc", [type_for_alloc], [ts.IntType(32)])


    f = sa.FunctionDefinition(
        "heap_init",
        ['type_for_alloc'],
        [f'_pos_{i}' for i in range(len(argument_types))],
        sa.TypePtrExpression(sa.TypeTypeExpression(type_for_alloc)),
        [
            sa.TypeDeclarationStatementFunction("_c", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("type_for_alloc"), 
                    "__eq__",
                    sa.TypeTypeExpression(type_for_alloc)
                )]
            ))] + checks +
        [
            sa.InitStatement(
                "assigned",
                sa.CallExpression(
                    "heap_alloc", 
                    [sa.TypeTypeExpression(type_for_alloc)],
                    [sa.IntLiteralExpression(1, 32)],
                )),
            sa.ExpressionStatement(
                sa.CallExpression("__init__",[],
                    [sa.IdExpression("assigned")]+[
                        sa.IdExpression(f"_pos_{i}") for i in range(len(argument_types))
                    ]
                )
            ),
            sa.ReturnStatement(sa.IdExpression("assigned")),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)

    return True

