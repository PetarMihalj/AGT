from typing import List

from . import inference_errors as ierr
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
    if name != "heap_alloc": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()

    if len(type_argument_types) != 1: raise ierr.TypeGenError()

    if not isinstance(argument_types[0], ts.IntType): raise ierr.TypeGenError()

    type_alloc = type_argument_types[0]
    type_size = argument_types[0]

    dname = tc.scope_man.new_func_name(f"dummy_heap_alloc_array")
    tc.primitives.append(prim.HeapAllocPrimitive(
        dname,
        type_alloc.mangled_name,
        type_size.mangled_name,
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.PointerType(type_alloc))
    return ft

@add_method_to_list(func_methods)
def gen_heap_free(tc, name: str,
                     type_argument_types: List[Type],
                     argument_types: List[Type],
            ):
    if name != "heap_free": raise ierr.TypeGenError()
    if len(argument_types) != 1: raise ierr.TypeGenError()
    if len(type_argument_types) != 0: raise ierr.TypeGenError()

    type_free_ptr = argument_types[0]
    if not isinstance(type_free_ptr, ts.PointerType): raise ierr.TypeGenError()

    type_free = type_free_ptr.pointed

    dname = tc.scope_man.new_func_name(f"dummy_heap_free")
    tc.primitives.append(prim.HeapFreePrimitive(
        dname,
        type_free.mangled_name,
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.VoidType())
    return ft



