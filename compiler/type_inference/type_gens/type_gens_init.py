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
def gen_heap_object(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "heap_object": raise ierr.TypeGenError()

    if len(type_argument_types) != 1: raise ierr.TypeGenError()
    init_type = type_argument_types[0]

    try:
        fn_alloc_mn = tc.resolve_function("heap_alloc", (init_type,), (ts.IntType(32),)).mangled_name
        fn_init_mn = tc.resolve_function("__init__", (), 
            (ts.PointerType(init_type),) + argument_types
        ).mangled_name
    except ierr.InferenceError:
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"heap_object")
    tc.code_blocks.append(prim.HeapObjectPrimitive(
        dname,
        init_type.mangled_name,
        [at.mangled_name for at in argument_types],
        fn_alloc_mn,
        fn_init_mn,
    ))

    ft = ts.FunctionType(
        dname, 
        ts.PointerType(init_type),
        do_not_copy_args = False,
    )
    return ft


@add_method_to_list(func_methods)
def gen_stack_object(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "object": raise ierr.TypeGenError()
    if len(type_argument_types) != 1: raise ierr.TypeGenError()

    init_type = type_argument_types[0]

    try:
        fn_init_mn = tc.resolve_function("__init__", (), 
            (ts.PointerType(init_type),) + argument_types
        ).mangled_name
    except ierr.InferenceError:
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"stack_object_struct")
    tc.code_blocks.append(prim.StackObjectPrimitive(
        dname,
        init_type.mangled_name,
        [at.mangled_name for at in argument_types],
        fn_init_mn,
    ))

    ft = ts.FunctionType(
        dname, 
        init_type,
        do_not_copy_args = False,
    )
    return ft

