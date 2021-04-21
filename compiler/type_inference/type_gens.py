from typing import List

from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts
from .recursive_logger import LogTypes

from ..semantics_parsing import semantic_ast as sa
# MAIN METHODS

func_methods = []
struct_methods = []

def gen_function(tc, name: str,
                 type_argument_types: List[Type],
                 argument_types: List[Type]
            ):
    if ((name, tuple(type_argument_types), tuple(argument_types))) in tc.gen_set:
        return
    tc.gen_set.add((name, tuple(type_argument_types), tuple(argument_types)))
    for sm in func_methods:
        if sm(tc,name,type_argument_types, argument_types):
            tc.logger.log("Function def autogenerated", LogTypes.FUNCTION_OR_STRUCT_DEFINITION)

def gen_struct(tc, name: str,
            type_argument_types: List[Type]
        ):
    if ((name, tuple(type_argument_types))) in tc.gen_set:
        return
    tc.gen_set.add((name, tuple(type_argument_types))) 
    for sm in struct_methods:
        if sm(tc,name,type_argument_types):
            tc.logger.log("Struct def autogenerated", LogTypes.FUNCTION_OR_STRUCT_DEFINITION)

# targets

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
    try:
        if name[0] == 'i':
            sign = 1
        elif name[0] == 'I':
            sign = -1
        else:
            return False
        val = int(name[1:])*sign

        tc.struct_type_container[(name, tuple(type_argument_types))] = ts.IntType(val)
        return True
    except:
        return False


@add_method_to_list(struct_methods)
def gen_int_type_ops(tc, name: str,
                 type_argument_types: List[Type],
            ):
    try:
        i1 = type_argument_types[0].size
        i2 = type_argument_types[1].size
        res = int(getattr(i1, name if name!="__div__" else "__floordiv__")(i2))
        tc.struct_type_container[(name, tuple(type_argument_types))] = ts.IntType(res)
        return True
    except:
        return False

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

    if tc.resolve_struct(name, type_argument_types, use_gens = False) is not None:
        return False

    if name=="__eq__":
        tc.struct_type_container[(name, tuple(type_argument_types))] = ts.IntType(int(t1 == t2))
        return True
    elif name=="__ne__":
        tc.struct_type_container[(name, tuple(type_argument_types))] = ts.IntType(int(t1 != t2))
        return True
    else:
        return False

##
##
## functions
##
##

# INT INITS

@add_method_to_list(func_methods)
def gen_int_init_default(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__init__": return False
    if len(type_argument_types)>0: return False

    if len(argument_types) != 2: return False
    if not isinstance(argument_types[0], ts.PointerType): return False
    pointed = argument_types[0].pointed
    if not isinstance(pointed, ts.IntType): return False
    size = pointed.size
    if size <= 0: return False

    if not isinstance(argument_types[1], ts.IntType): return False
    if argument_types[1].size != size: return False

    f = sa.FunctionDefinition(
        "__init__",
        [],
        ["ptr", "val"],
        sa.TypeIdExpression("void"),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("ptr"), 
                    "__eq__",
                    sa.TypeTypeExpression(argument_types[0])
                )]
            )),
            sa.TypeDeclarationStatementFunction("_2", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("val"), 
                    "__eq__",
                    sa.TypeTypeExpression(argument_types[1])
                )]
            )),
            sa.AssignmentStatement(sa.DerefExpression(sa.IdExpression("ptr")), sa.IdExpression("val")),
            sa.ReturnStatement(None),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)
    return True

@add_method_to_list(func_methods)
def gen_int_dest_default(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__dest__": return False
    if len(type_argument_types)>0: return False

    if len(argument_types) != 1: return False
    if not isinstance(argument_types[0], ts.PointerType): return False
    pointed = argument_types[0].pointed
    if not isinstance(pointed, ts.IntType): return False
    size = pointed.size
    if size <= 0: return False

    f = sa.FunctionDefinition(
        "__init__",
        [],
        ["ptr"],
        sa.TypeIdExpression("void"),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("ptr"), 
                    "__eq__",
                    sa.TypePtrExpression(sa.TypeIdExpression(f"i{size}"))
                )]
            )),
            sa.ReturnStatement(None),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)
    return True


@add_method_to_list(func_methods)
def gen_int_copy_default(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__copy__": return False
    if len(type_argument_types)>0: return False

    if len(argument_types) != 2: return False

    if not isinstance(argument_types[0], ts.PointerType): return False
    pointed1 = argument_types[0].pointed
    if not isinstance(pointed1, ts.IntType): return False
    size1 = pointed1.size
    if size1 <= 0: return False


    if not isinstance(argument_types[1], ts.PointerType): return False
    pointed2 = argument_types[1].pointed
    if not isinstance(pointed2, ts.IntType): return False
    size2 = pointed2.size
    if size2 <= 0: return False

    if size1 != size2:
        return False

    f = sa.FunctionDefinition(
        "__copy__",
        [],
        ["ptr_dest", "ptr_src"],
        sa.TypeIdExpression("void"),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("ptr_dest"), 
                    "__eq__",
                    sa.TypePtrExpression(sa.TypeIdExpression(f"i{size1}"))
                )]
            )),
            sa.TypeDeclarationStatementFunction("_2", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("ptr_src"),
                    "__eq__",
                    sa.TypePtrExpression(sa.TypeIdExpression(f"i{size2}"))
                )]
            )),
            sa.MemoryCopyStatement("ptr_dest", "ptr_src"),
            sa.ReturnStatement(None),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)
    return True

# -------------



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


@add_method_to_list(func_methods)
def gen_heap_alloc(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "heap_alloc": return False
    if len(argument_types)!=1: return False

    if len(type_argument_types) != 1: return False

    if not isinstance(argument_types[0], ts.IntType): return False

    type_alloc = type_argument_types[0].size
    type_size = argument_types[0].size


    f = sa.FunctionDefinition(
        "heao_alloc",
        ['type_alloc'],
        ['size'],
        sa.TypePtrExpression(TypeIdExpression(f"{type_alloc}")),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("type_alloc"), 
                    "__eq__",
                    sa.TypeIdExpression(f"{type_alloc}")
                )]
            )),
            sa.TypeDeclarationStatementFunction("_2", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("size"), 
                    "__eq__",
                    sa.TypeIdExpression(f"{size}")
                )]
            )),

            sa.HeapAllocStatement("mem", 
                sa.TypeIdExpression(f"{type_alloc}"), 
                sa.IdExpression("size")
            ),
            sa.ReturnStatement(sa.IdExpression("mem")),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)
    return True

# struct init, copy, dest

@add_method_to_list(func_methods)
def gen_init_struct(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__init__": return False
    if len(type_argument_types)>0: return False

    if len(argument_types) == 0: return False
    if not isinstance(argument_types[0], ts.PointerType): return False
    pointed = argument_types[0].pointed
    if not isinstance(pointed, ts.StructType): return False
    pointed: ts.StructType

    if len(argument_types)-1 != len(pointed.members): return False

    if tc.resolve_function(
            name, type_argument_types, 
            argument_types, use_gens = False) is not None:
        return False

    checks_mems = [
        sa.TypeDeclarationStatementFunction(f"_{i}", sa.TypeAngleExpression("enable_if", 
            [sa.TypeBinaryExpression(
                sa.TypeIdExpression(f"_part_{i}"), 
                "__eq__",
                sa.TypeTypeExpression(argument_types[i])
            )]
        )) for i in range(1,len(argument_types))
    ]

    init_mems = [
            sa.ExpressionStatement(sa.CallExpression("__init__", [], [
                sa.AddressExpression(sa.MemberIndexExpression(
                    sa.DerefExpression(sa.IdExpression("ptr")),
                    name
                )),
                sa.IdExpression(f"_part_{i+1}"),
            ]
            )) for i,name in enumerate(pointed.members) 
    ]

    f = sa.FunctionDefinition(
        "__init__",
        [],
        ["ptr"]+[f"_part_{i}" for i in range(1,len(argument_types))],
        sa.TypeIdExpression("void"),
        [
            sa.TypeDeclarationStatementFunction("_0", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("ptr"), 
                    "__eq__",
                    sa.TypeTypeExpression(argument_types[0])
                )]
            )),
        ] + checks_mems + init_mems + [
            sa.ReturnStatement(None),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)
    return True

@add_method_to_list(func_methods)
def gen_copy_struct(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__init__": return False
    if len(type_argument_types)>0: return False

    if len(argument_types) != 2: return False

    if not isinstance(argument_types[0], ts.PointerType): return False
    pointed1 = argument_types[0].pointed
    if not isinstance(pointed1, ts.StructType): return False
    pointed1: ts.StructType

    if not isinstance(argument_types[1], ts.PointerType): return False
    pointed2 = argument_types[0].pointed
    if not isinstance(pointed2, ts.StructType): return False
    pointed2: ts.StructType

    if pointed1 != pointed2:
        return False

    if tc.resolve_function(
            name, type_argument_types, 
            argument_types, use_gens = False) is not None:
        return False

    copy_mems = [
            sa.ExpressionStatement(sa.CallExpression("__copy__", [], [
                sa.AddressExpression(sa.MemberIndexExpression(
                    sa.DerefExpression(sa.IdExpression("ptr_dest")),
                    name
                )),
                sa.AddressExpression(sa.MemberIndexExpression(
                    sa.DerefExpression(sa.IdExpression("ptr_src")),
                    name
                )),
            ]
            )) for i,name in enumerate(pointed.members) 
    ]

    f = sa.FunctionDefinition(
        "__init__",
        [],
        ["ptr_dest", "ptr_src"],
        sa.TypeIdExpression("void"),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("ptr_dest"), 
                    "__eq__",
                    sa.TypeTypeExpression(argument_types[0])
                )]
            )),
            sa.TypeDeclarationStatementFunction("_2", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("ptr_src"), 
                    "__eq__",
                    sa.TypeTypeExpression(argument_types[1])
                )]
            )),
        ] + copy_mems + [
            sa.ReturnStatement(None),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)
    return True

@add_method_to_list(func_methods)
def gen_dest_struct(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__init__": return False
    if len(type_argument_types)>0: return False

    if len(argument_types) != 1: return False
    if not isinstance(argument_types[0], ts.PointerType): return False
    pointed = argument_types[0].pointed
    if not isinstance(pointed, ts.StructType): return False
    pointed: ts.StructType

    if tc.resolve_function(
            name, type_argument_types, 
            argument_types, use_gens = False) is not None:
        return False


    dest_mems = [
            sa.ExpressionStatement(sa.CallExpression("__dest__", [], [
                sa.AddressExpression(sa.MemberIndexExpression(
                    sa.DerefExpression(sa.IdExpression("ptr")),
                    name
                ))
            ]
            )) for i,name in enumerate(pointed.members) 
    ]

    f = sa.FunctionDefinition(
        "__init__",
        [],
        ["ptr"],
        sa.TypeIdExpression("void"),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("ptr"), 
                    "__eq__",
                    sa.TypeTypeExpression(argument_types[0])
                )]
            )),
        ] + dest_mems + [
            sa.ReturnStatement(None),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)
    return True
