from typing import List

from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts
from .recursive_logger import LogTypes

from ..semantics_parsing import semantic_ast as sa

from .type_gens import func_methods, struct_methods

@add_method_to_list(func_methods)
def gen_type_to_value(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "type_to_value": return False
    if len(argument_types)>0: return False

    if len(type_argument_types) != 2: return False

    if not isinstance(type_argument_types[0], ts.IntType): return False
    if not isinstance(type_argument_types[1], ts.IntType): return False
    val = type_argument_types[0].size
    size = type_argument_types[1].size


    f = sa.FunctionDefinition(
        "type_to_value",
        ["val", "size"],
        [],
        sa.TypeIdExpression(f"i{size}"),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("val"), 
                    "__eq__",
                    sa.TypeIdExpression(f"{val}")
                )]
            )),
            sa.TypeDeclarationStatementFunction("_2", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("size"), 
                    "__eq__",
                    sa.TypeIdExpression(f"{size}")
                )]
            )),
            sa.ReturnStatement(sa.IntLiteralExpression(val, size))
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)
    return True


@add_method_to_list(struct_methods)
def gen_void_type(tc, name: str,
                 type_argument_types: List[Type],
            ):
    if name == "void" and len(type_argument_types)==0:
        tc.struct_type_container[(name, tuple(type_argument_types))] = ts.VoidType()
        return True
    else:
        return False


@add_method_to_list(struct_methods)
def gen_int_type(tc, name: str,
                 type_argument_types: List[Type],
            ):
    if len(name)==0:
        return False
    if len(type_argument_types)!=0:
        return False
    if name[0] != 'i':
        return False
    
    try:
        val = int(name[1:])
    except:
        return False

    if val in [8,16,32,64]:
        tc.struct_type_container[(name, tuple(type_argument_types))] = ts.IntType(val)
        return True
    else:
        return False

@add_method_to_list(struct_methods)
def gen_bool_type(tc, name: str,
                 type_argument_types: List[Type],
            ):
    if name!='bool':
        return False
    if len(type_argument_types)!=0:
        return False
    
    tc.struct_type_container[(name, tuple(type_argument_types))] = ts.BoolType()
    return True

@add_method_to_list(struct_methods)
def gen_int_type_ops(tc, name: str,
                 type_argument_types: List[Type],
            ):
    if name not in sa.ops_mapping.values():
        return False
    if len(type_argument_types) != 2:
        return False
    if not isinstance(type_argument_types[0], ts.IntType):
        return False
    if not isinstance(type_argument_types[1], ts.IntType):
        return False

    i1 = type_argument_types[0].size
    i2 = type_argument_types[1].size
    try:
        res = int(getattr(i1, name if name!="__div__" else "__floordiv__")(i2))
    except:
        return False

    tc.struct_type_container[(name, tuple(type_argument_types))] = ts.IntType(res)
    return True

@add_method_to_list(struct_methods)
def gen_enable_if_type(tc, name: str,
                 type_argument_types: List[Type],
            ):
    if name != 'enable_if':
        return False
    if len(type_argument_types) != 1:
        return False
    if not isinstance(type_argument_types[0], ts.IntType):
        return False

    if type_argument_types[0].size != 0:
        tc.struct_type_container[(name, tuple(type_argument_types))] = ts.IntType(1)
        return True
    else:
        return False

@add_method_to_list(struct_methods)
def gen_type_ops(tc, name: str,
                 type_argument_types: List[Type],
            ):
    if len(type_argument_types) != 2:
        return False
    t1 = type_argument_types[0]
    t2 = type_argument_types[1]

    # because there is a specialization for this already in gens
    if isinstance(type_argument_types[0], ts.IntType):
        return False
    if isinstance(type_argument_types[1], ts.IntType):
        return False

    if name=="__eq__":
        tc.struct_type_container[(name, tuple(type_argument_types))] = ts.IntType(int(t1 == t2))
        return True
    elif name=="__ne__":
        tc.struct_type_container[(name, tuple(type_argument_types))] = ts.IntType(int(t1 != t2))
        return True
    else:
        return False
