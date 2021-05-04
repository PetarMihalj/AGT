from typing import List

from . import inference_errors as ierr
from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts

from ..semantics_parsing import semantic_ast as sa

from .type_gens import func_methods, struct_methods

@add_method_to_list(func_methods)
def gen_heap_object(tc, name: str,
                     type_argument_types: List[Type],
                     argument_types: List[Type],
            ):
    if name != "heap_object": raise ierr.TypeGenError()

    if len(type_argument_types) != 1: raise ierr.TypeGenError()
    init_type = type_argument_types[0]

    types_mn = []
    if isinstance(init_type, ts.StructType): 
        if len(argument_types) != len(init_type.members): raise ierr.TypeGenError()
        for t1, m in zip(argument_types, init_type.members):
            t2 = init_type.types[m]
            if t1!=t2:
                raise ierr.TypeGenError()
            types_mn.append(t2.mangled_name)
    else:
        if len(argument_types) != 1: raise ierr.TypeGenError()
        if argument_types[0] != init_type: raise ierr.TypeGenError()
        types_mn = [init_type.mangled_name]

    try:
        fn_alloc_mn = tc.resolve_function("heap_alloc", [init_type], [ts.IntType(32)]).mangled_name
        print("A")
        fn_init_mn = tc.resolve_function("__init__", [], 
            [ts.PointerType(init_type)] + argument_types
        ).mangled_name
        print("B")
    except ierr.InferenceError:
        raise ierr.TypeGenError()


    dname = tc.scope_man.new_func_name(f"heap_object")
    tc.primitives.append(prim.HeapObjectPrimitive(
        dname,
        init_type.mangled_name,
        types_mn,
        fn_alloc_mn,
        fn_init_mn,
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.PointerType(init_type))
    init_type.needs_gen = True
    return ft


@add_method_to_list(func_methods)
def gen_stack_object(tc, name: str,
                     type_argument_types: List[Type],
                     argument_types: List[Type],
            ):
    if name != "object": raise ierr.TypeGenError()
    if len(type_argument_types) != 1: raise ierr.TypeGenError()

    init_type = type_argument_types[0]

    types_mn = []
    if isinstance(init_type, ts.StructType): 
        if len(argument_types) != len(init_type.members): raise ierr.TypeGenError()
        for t1, m in zip(argument_types, init_type.members):
            t2 = init_type.types[m]
            if t1!=t2:
                raise ierr.TypeGenError()
            types_mn.append(t2.mangled_name)
    else:
        if len(argument_types) != 1: raise ierr.TypeGenError()
        if argument_types[0] != init_type: raise ierr.TypeGenError()
        types_mn = [init_type.mangled_name]

    try:
        fn_init_mn = tc.resolve_function("__init__", [], 
            [ts.PointerType(init_type)] + argument_types
        ).mangled_name
    except ierr.InferenceError:
        raise ierr.TypeGenError()


    dname = tc.scope_man.new_func_name(f"stack_object_struct")
    tc.primitives.append(prim.StackObjectPrimitive(
        dname,
        init_type.mangled_name,
        types_mn,
        fn_init_mn,
    ))

    ft = ts.FunctionTypePrimitive(dname, init_type)
    init_type.needs_gen = True
    return ft

