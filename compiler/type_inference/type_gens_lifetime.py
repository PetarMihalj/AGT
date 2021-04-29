from typing import List

from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts
from .recursive_logger import LogTypes

from ..semantics_parsing import semantic_ast as sa

from .type_gens import func_methods, struct_methods


# builtin lifetime constructs


@add_method_to_list(func_methods)
def gen_builtin_init(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__init__": return False
    if len(type_argument_types)>0: return False
    if len(argument_types) != 2: return False

    if not isinstance(argument_types[0], ts.PointerType): return False
    pointed = argument_types[0].pointed
    val=argument_types[1]

    if pointed != val:
        return False

    allowed = [ts.IntType(i) for i in [8,16,32,64]] + [ts.BoolType()]
    if val not in allowed and not isinstance(val, ts.PointerType):
        return False

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
                    sa.TypeTypeExpression(val)
                )]
            )),
            sa.InitStatement("val_addr", sa.AddressExpression(sa.IdExpression("val"))),
            sa.MemoryCopyStatement("ptr", "val_addr"),
            sa.ReturnStatement(None),
        ]
    )
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)

    return True


@add_method_to_list(func_methods)
def gen_builtin_copy(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__copy__": return False
    if len(type_argument_types)>0: return False

    if len(argument_types) != 2: return False

    if not isinstance(argument_types[0], ts.PointerType): return False
    if not isinstance(argument_types[1], ts.PointerType): return False

    ptr_dest = argument_types[0]
    ptr_src = argument_types[1]
    if ptr_dest != ptr_src:
        return False

    allowed = [ts.IntType(i) for i in [8,16,32,64]] + [ts.BoolType()]
    if (ptr_dest.pointed not in allowed and not isinstance(ptr_dest.pointed, ts.PointerType)):
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
                    sa.TypeTypeExpression(ptr_dest)
                )]
            )),
            sa.TypeDeclarationStatementFunction("_2", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("ptr_src"),
                    "__eq__",
                    sa.TypeTypeExpression(ptr_src)
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

@add_method_to_list(func_methods)
def gen_builtin_dest(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__dest__": return False
    if len(type_argument_types)>0: return False

    if len(argument_types) != 1: return False

    if not isinstance(argument_types[0], ts.PointerType): return False

    ptr = argument_types[0]

    allowed = [ts.IntType(i) for i in [8,16,32,64]] + [ts.BoolType()]
    if (ptr.pointed not in allowed and not isinstance(ptr.pointed, ts.PointerType)):
        return False

    f = sa.FunctionDefinition(
        "__dest__",
        [],
        ["ptr"],
        sa.TypeIdExpression("void"),
        [
            sa.TypeDeclarationStatementFunction("_1", sa.TypeAngleExpression("enable_if", 
                [sa.TypeBinaryExpression(
                    sa.TypeIdExpression("ptr"), 
                    "__eq__",
                    sa.TypeTypeExpression(ptr)
                )]
            )),
            sa.ReturnStatement(None),
        ]
    )
    f.do_not_dest_params = True
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)
    return True


# STRUCT lifetime constructs

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
    f.default_ignore_when_other_available = True
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)
    return True

@add_method_to_list(func_methods)
def gen_copy_struct(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__copy__": return False
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
            )) for i,name in enumerate(pointed1.members) 
    ]

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
    f.default_ignore_when_other_available = True
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)
    return True

@add_method_to_list(func_methods)
def gen_dest_struct(tc, name: str,
                         type_argument_types: List[Type],
                         argument_types: List[Type],
            ):
    if name != "__dest__": return False
    if len(type_argument_types)>0: return False

    if len(argument_types) != 1: return False
    if not isinstance(argument_types[0], ts.PointerType): return False
    pointed = argument_types[0].pointed
    if not isinstance(pointed, ts.StructType): return False
    pointed: ts.StructType

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
        "__dest__",
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
    f.default_ignore_when_other_available = True
    f.linespan = (-1,-1)
    f.lexspan = (-1,-1)
    tc.func_defs.append(f)
    return True

