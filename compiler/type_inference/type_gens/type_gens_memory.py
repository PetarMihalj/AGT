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
def gen_heap_alloc(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "heap_alloc": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()

    if len(type_argument_types) != 1: raise ierr.TypeGenError()

    if not isinstance(argument_types[0], ts.IntType): raise ierr.TypeGenError()

    type_alloc = type_argument_types[0]
    type_size = argument_types[0]

    dname = tc.scope_man.new_func_name(f"dummy_heap_alloc_array")
    tc.code_blocks.append(prim.HeapAllocPrimitive(
        dname,
        type_alloc.mangled_name,
        type_size.mangled_name,
    ))

    ft = ts.FunctionType(
        dname, 
        ts.PointerType(type_alloc),
        do_not_copy_args = False,
    )
    return ft

@add_method_to_list(func_methods)
def gen_heap_free(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "heap_free": raise ierr.TypeGenError()
    if len(argument_types) != 1: raise ierr.TypeGenError()
    if len(type_argument_types) != 0: raise ierr.TypeGenError()

    type_free_ptr = argument_types[0]
    if not isinstance(type_free_ptr, ts.PointerType): raise ierr.TypeGenError()

    type_free = type_free_ptr.pointed

    dname = tc.scope_man.new_func_name(f"dummy_heap_free")
    tc.code_blocks.append(prim.HeapFreePrimitive(
        dname,
        type_free.mangled_name,
    ))

    ft = ts.FunctionType(
        dname, 
        None,
        do_not_copy_args = False,
    )
    return ft



