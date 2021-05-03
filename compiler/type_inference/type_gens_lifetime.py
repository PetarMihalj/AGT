from typing import List

from . import inference_errors as ierr
from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts

from ..semantics_parsing import semantic_ast as sa

from .type_gens import func_methods, struct_methods

# builtin lifetime constructs

@add_method_to_list(func_methods)
def gen_builtin_init(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__init__": raise ierr.TypeGenError()
    if len(type_argument_types)>0: raise ierr.TypeGenError()
    if len(argument_types) != 2: raise ierr.TypeGenError()

    if not isinstance(argument_types[0], ts.PointerType): raise ierr.TypeGenError()
    pointed = argument_types[0].pointed
    val=argument_types[1]

    if pointed != val:
        raise ierr.TypeGenError()

    allowed = [ts.IntType(i) for i in [8,16,32,64]] + [ts.BoolType()]
    if val not in allowed and not isinstance(val, ts.PointerType):
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"builtin_init")
    tc.primitives.append(prim.DefaultBuiltinInitPrimitive(
        dname,
        pointed.mangled_name
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.VoidType())
    return ft


@add_method_to_list(func_methods)
def gen_builtin_copy(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__copy__": raise ierr.TypeGenError()
    if len(type_argument_types)>0: raise ierr.TypeGenError()

    if len(argument_types) != 2: raise ierr.TypeGenError()

    if not isinstance(argument_types[0], ts.PointerType): raise ierr.TypeGenError()
    if not isinstance(argument_types[1], ts.PointerType): raise ierr.TypeGenError()

    ptr_dest = argument_types[0]
    ptr_src = argument_types[1]
    if ptr_dest != ptr_src:
        raise ierr.TypeGenError()

    allowed = [ts.IntType(i) for i in [8,16,32,64]] + [ts.BoolType()]
    if (ptr_dest.pointed not in allowed and not isinstance(ptr_dest.pointed, ts.PointerType)):
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"builtin_copy")
    tc.primitives.append(prim.DefaultBuiltinCopyPrimitive(
        dname,
        ptr_dest.pointed.mangled_name
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.VoidType())
    return ft

@add_method_to_list(func_methods)
def gen_builtin_dest(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__dest__": raise ierr.TypeGenError()
    if len(type_argument_types)>0: raise ierr.TypeGenError()

    if len(argument_types) != 1: raise ierr.TypeGenError()

    if not isinstance(argument_types[0], ts.PointerType): raise ierr.TypeGenError()

    ptr = argument_types[0]

    allowed = [ts.IntType(i) for i in [8,16,32,64]] + [ts.BoolType()]
    if (ptr.pointed not in allowed and not isinstance(ptr.pointed, ts.PointerType)):
        raise ierr.TypeGenError()

    
    dname = tc.scope_man.new_func_name(f"func_do_nothing")
    tc.primitives.append(prim.DefaultBuiltinDestPrimitive(
        dname,
        [ptr.mangled_name]
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.VoidType())
    return ft


# STRUCT lifetime constructs

@add_method_to_list(func_methods)
def gen_struct_init(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__init__": raise ierr.TypeGenError()
    if len(type_argument_types)>0: raise ierr.TypeGenError()

    if len(argument_types) == 0: raise ierr.TypeGenError()
    if not isinstance(argument_types[0], ts.PointerType): raise ierr.TypeGenError()
    pointed = argument_types[0].pointed
    if not isinstance(pointed, ts.StructType): raise ierr.TypeGenError()
    pointed: ts.StructType

    if len(argument_types)-1 != len(pointed.members): raise ierr.TypeGenError()

    for t1, m in zip(argument_types[1:], pointed.members):
        t2 = pointed.types[m]
        if t1!=t2:
            raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"dummy_init_struct")
    tc.primitives.append(prim.DefaultStructInitPrimitive(
        dname,
        pointed.mangled_name,
        [a.mangled_name for a in argument_types[1:]],
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.VoidType())
    pointed.needs_gen = True
    return ft

@add_method_to_list(func_methods)
def gen_struct_copy(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__copy__": raise ierr.TypeGenError()
    if len(type_argument_types)>0: raise ierr.TypeGenError()

    if len(argument_types) != 2: raise ierr.TypeGenError()

    if not isinstance(argument_types[0], ts.PointerType): raise ierr.TypeGenError()
    pointed1 = argument_types[0].pointed
    if not isinstance(pointed1, ts.StructType): raise ierr.TypeGenError()
    pointed1: ts.StructType

    if not isinstance(argument_types[1], ts.PointerType): raise ierr.TypeGenError()
    pointed2 = argument_types[0].pointed
    if not isinstance(pointed2, ts.StructType): raise ierr.TypeGenError()
    pointed2: ts.StructType

    copy_calls_mn = []
    member_types_mn = []
    for m in pointed1.members:
        t = pointed1.types[m]
        member_types_mn.append(t.mangled_name)
        try:
            cf = tc.resolve_function(
                    "__copy__",
                    [],
                    [ts.PointerType(t)]*2,
            )
            copy_calls_mn.append(cf.mangled_name)
        except ierr.InferenceError:
            raise ierr.TypeGenError()


    dname = tc.scope_man.new_func_name(f"dummy_copy_struct")
    tc.primitives.append(prim.DefaultStructCopyPrimitive(
        dname,
        pointed1.mangled_name,
        member_types_mn,
        copy_calls_mn,
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.VoidType())
    pointed1.needs_gen = True
    return ft


@add_method_to_list(func_methods)
def gen_struct_dest(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__dest__": raise ierr.TypeGenError()
    if len(type_argument_types)>0: raise ierr.TypeGenError()

    if len(argument_types) != 1: raise ierr.TypeGenError()
    if not isinstance(argument_types[0], ts.PointerType): raise ierr.TypeGenError()
    pointed = argument_types[0].pointed
    if not isinstance(pointed, ts.StructType): raise ierr.TypeGenError()
    pointed: ts.StructType


    dest_calls_mn = []
    member_types_mn = []
    for m in pointed.members:
        t = pointed.types[m]
        member_types_mn.append(t.mangled_name)
        try:
            cf = tc.resolve_function(
                "__dest__",
                [],
                [ts.PointerType(t)],
            )
            dest_calls_mn.append(cf.mangled_name)
        except ierr.InferenceError:
            raise ierr.TypeGenError()


    dname = tc.scope_man.new_func_name(f"dummy_dest_struct")
    tc.primitives.append(prim.DefaultStructDestPrimitive(
        dname,
        pointed.mangled_name,
        member_types_mn,
        dest_calls_mn,
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.VoidType())
    return ft

