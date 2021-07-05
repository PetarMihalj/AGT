from typing import Tuple, List
from dataclasses import dataclass

from .. import inference_errors as ierr
from .. import type_system as ts
from .. import context
from ..code_blocks import Primitive 
from ..type_engine import TypingContext

from . import func_methods, concrete_methods, add_method_to_list

# ---------------------------------------------------------------------

@add_method_to_list(func_methods)
def gen_in_intbool(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "in": raise ierr.TypeGenError()
    if len(argument_types)!=0: raise ierr.TypeGenError()
    if len(type_argument_types) != 1: raise ierr.TypeGenError()

    type_arg = type_argument_types[0]
    if isinstance(type_arg,ts.IntType):
        size = type_arg.size
    elif isinstance(type_arg, ts.BoolType):
        size = 1
    else:
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"in_i{size}_dummy")
    tc.code_blocks.append(InIntBoolPrimitive(
        dname,
        size
    ))

    ft = ts.FunctionType(
        dname, 
        ts.IntType(size) if size>1 else ts.BoolType(),
        do_not_copy_args = False,
    )
    return ft

@dataclass
class InIntBoolPrimitive(Primitive):
    mangled_name: str
    size: int
    def get_code(self):
        if self.size<64:
            return [
                f"; Function Attrs: nounwind sspstrong uwtable",
                f"define dso_local i{self.size} @{self.mangled_name}() local_unnamed_addr #0 {{",
                f"  %1 = alloca i64, align 8",
                f"  %2 = bitcast i64* %1 to i8*",
                f"  %3 = call i32 (i8*, ...) @__isoc99_scanf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.in_int_str, i64 0, i64 0), i64* nonnull %1)",
                f"  %4 = load i64, i64* %1, align 8",
                f"  %5 = trunc i64 %4 to i{self.size}",
                f"  ret i{self.size} %5",
                f"}}",
            ]
        else:
            return [
                f"; Function Attrs: nounwind sspstrong uwtable",
                f"define dso_local i{self.size} @{self.mangled_name}() local_unnamed_addr #0 {{",
                f"  %1 = alloca i64, align 8",
                f"  %2 = bitcast i64* %1 to i8*",
                f"  %3 = call i32 (i8*, ...) @__isoc99_scanf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.in_int_str, i64 0, i64 0), i64* nonnull %1)",
                f"  %4 = load i64, i64* %1, align 8",
                f"  ret i{self.size} %4",
                f"}}",
            ]

# ---------------------------------------------------------------------

@add_method_to_list(func_methods)
def gen_out_intbool(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "out": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()
    if len(type_argument_types) != 0: raise ierr.TypeGenError()

    type_arg = argument_types[0]
    if isinstance(type_arg,ts.IntType):
        size = type_arg.size
    elif isinstance(type_arg, ts.BoolType):
        size = 1
    else:
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"out_i{size}_dummy")
    tc.code_blocks.append(OutIntBoolPrimitive(
        dname,
        size
    ))

    ft = ts.FunctionType(
        dname, 
        None,
        do_not_copy_args = False,
    )
    return ft

@dataclass
class OutIntBoolPrimitive(Primitive):
    mangled_name: str
    size: int
    def get_code(self):
        if self.size == 1:
            return [
                f"; Function Attrs: nofree nounwind sspstrong uwtable",
                f"define dso_local void @{self.mangled_name}(i{self.size} %0) local_unnamed_addr #0 {{",
                f"  %2 = zext i{self.size} %0 to i64",
                f"  %3 = tail call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([5 x i8], [5 x i8]* @.out_int_str, i64 0, i64 0), i64 %2)",
                f"  ret void",
                f"}}",
            ]
        elif self.size < 64:
            return [
                f"; Function Attrs: nofree nounwind sspstrong uwtable",
                f"define dso_local void @{self.mangled_name}(i{self.size} %0) local_unnamed_addr #0 {{",
                f"  %2 = sext i{self.size} %0 to i64",
                f"  %3 = tail call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([5 x i8], [5 x i8]* @.out_int_str, i64 0, i64 0), i64 %2)",
                f"  ret void",
                f"}}",
            ]
        else:
            return [
                f"; Function Attrs: nofree nounwind sspstrong uwtable",
                f"define dso_local void @{self.mangled_name}(i{self.size} %0) local_unnamed_addr #0 {{",
                f"  %2 = tail call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([5 x i8], [5 x i8]* @.out_int_str, i64 0, i64 0), i64 %0)",
                f"  ret void",
                f"}}",
            ]

# ---------------------------------------------------------------------

@add_method_to_list(func_methods)
def gen_out_char(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "out": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()
    if len(type_argument_types) != 0: raise ierr.TypeGenError()

    type_arg = argument_types[0]
    if not isinstance(type_arg,ts.CharType):
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"out_char_dummy")
    tc.code_blocks.append(OutCharPrimitive(
        dname,
    ))

    ft = ts.FunctionType(
        dname, 
        None,
        do_not_copy_args = False,
    )
    return ft

@dataclass
class OutCharPrimitive(Primitive):
    mangled_name: str
    def get_code(self):
        return [
            f"; Function Attrs: noinline nounwind optnone sspstrong uwtable",
            f"define dso_local void @{self.mangled_name}(i8 signext %0) #0 {{",
            f"  %2 = alloca i8, align 1",
            f"  store i8 %0, i8* %2, align 1",
            f"  %3 = load i8, i8* %2, align 1",
            f"  %4 = sext i8 %3 to i32",
            f"  %5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.out_char_str, i64 0, i64 0), i32 %4)",
            f"  ret void",
            f"}}"
        ]

# ---------------------------------------------------------------------

@add_method_to_list(func_methods)
def gen_out_chararray(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "out": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()
    if len(type_argument_types) != 0: raise ierr.TypeGenError()

    type_arg = argument_types[0]
    if not isinstance(type_arg,ts.PointerType) or not isinstance(type_arg.pointed,ts.CharType):
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"out_char_dummy")
    tc.code_blocks.append(OutCharArrayPrimitive(
        dname,
    ))

    ft = ts.FunctionType(
        dname, 
        None,
        do_not_copy_args = False,
    )
    return ft

@dataclass
class OutCharArrayPrimitive(Primitive):
    mangled_name: str
    def get_code(self):
        return [
            f"; Function Attrs: noinline nounwind optnone sspstrong uwtable",
            f"define dso_local void @{self.mangled_name}(i8* %0) #0 {{",
            f"  %2 = alloca i8*, align 8",
            f"  store i8* %0, i8** %2, align 8",
            f"  %3 = load i8*, i8** %2, align 8",
            f"  %4 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.out_chararray_str, i64 0, i64 0), i8* %3)",
            f"  ret void",
            f"}}",
        ]


