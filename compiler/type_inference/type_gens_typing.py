from typing import List

from . import inference_errors as ierr
from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts

from ..semantics_parsing import semantic_ast as sa

from .type_gens import func_methods, struct_methods

@add_method_to_list(func_methods)
def gen_type_to_value(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "type_to_value": raise ierr.TypeGenError()
    if len(argument_types)>0: raise ierr.TypeGenError()

    if len(type_argument_types) != 2: raise ierr.TypeGenError()

    if not isinstance(type_argument_types[0], ts.IntType): raise ierr.TypeGenError()
    if not isinstance(type_argument_types[1], ts.IntType): raise ierr.TypeGenError()
    val = type_argument_types[0].size
    size = type_argument_types[1].size

    dname = tc.scope_man.new_func_name(f"dummy_ttv_{val}i{size}")
    tc.primitives.append(prim.TypeToValuePrimitive(
        dname,
        val,
        size,
    ))

    ft = ts.FunctionTypePrimitive(dname, ts.IntType(size))
    return ft


@add_method_to_list(struct_methods)
def gen_void_type(tc, name: str,
                 type_argument_types: List[Type],
            ):
    if name != "void": 
        raise ierr.TypeGenError()
    if len(type_argument_types)!=0:
        raise ierr.TypeGenError()

    return ts.VoidType()


@add_method_to_list(struct_methods)
def gen_int_type(tc, name: str,
                 type_argument_types: List[Type],
            ):
    if len(name)==0:
        raise ierr.TypeGenError()
    if len(type_argument_types)!=0:
        raise ierr.TypeGenError()
    if name[0] != 'i':
        raise ierr.TypeGenError()
    
    try:
        size = int(name[1:])
    except:
        raise ierr.TypeGenError()

    return ts.IntType(size)

@add_method_to_list(struct_methods)
def gen_bool_type(tc, name: str,
                 type_argument_types: List[Type],
            ):
    if name!='bool':
        raise ierr.TypeGenError()
    if len(type_argument_types)!=0:
        raise ierr.TypeGenError()
    
    return ts.BoolType()

@add_method_to_list(struct_methods)
def gen_int_type_ops(tc, name: str,
                 type_argument_types: List[Type],
            ):
    if name not in sa.ops_mapping.values():
        raise ierr.TypeGenError()
    if len(type_argument_types) != 2:
        raise ierr.TypeGenError()
    if not isinstance(type_argument_types[0], ts.IntType):
        raise ierr.TypeGenError()
    if not isinstance(type_argument_types[1], ts.IntType):
        raise ierr.TypeGenError()

    i1 = type_argument_types[0].size
    i2 = type_argument_types[1].size
    try:
        res = int(getattr(i1, name if name!="__div__" else "__floordiv__")(i2))
    except:
        raise ierr.TypeGenError()

    return ts.IntType(res)

@add_method_to_list(struct_methods)
def gen_type_ops(tc, name: str,
                 type_argument_types: List[Type],
            ):
    if len(type_argument_types) != 2:
        raise ierr.TypeGenError()
    t1 = type_argument_types[0]
    t2 = type_argument_types[1]

    # because there is a specialization for this already in gens
    if isinstance(type_argument_types[0], ts.IntType):
        raise ierr.TypeGenError()
    if isinstance(type_argument_types[1], ts.IntType):
        raise ierr.TypeGenError()

    if name=="__eq__":
        return ts.IntType(int(t1 == t2))
    elif name=="__ne__":
        return ts.IntType(int(t1 != t2))
    else:
        raise ierr.TypeGenError()
