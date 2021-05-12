from dataclasses import dataclass
from typing import List, Tuple

from . import type_system as ts
from . import code_blocks
from .code_blocks import Primitive


#
#
# DEFAULT PRIMITIVES
#
#

@dataclass
class DefaultStructInitPrimitive(Primitive):
    fn_mn: str
    type_struct_mn: str
    types_mn: List[str]

    def get_code(self):
        n = len(self.types_mn)

        args = ", ".join([f"%{self.types_mn[i]} %t_{i+1}" for i in range(n)])

        copies = []
        for i in range(n):
            copies.append(f"  %t_{n+i+1} = getelementptr inbounds %{self.type_struct_mn}, %{self.type_struct_mn}* %0, i64 0, i32 {i}")
            copies.append(f"  store %{self.types_mn[i]} %t_{i+1}, %{self.types_mn[i]}* %t_{n+i+1}")

        return [
                f"; Function Attrs: nofree norecurse nounwind sspstrong uwtable writeonly",
                f"define dso_local void @{self.fn_mn}(%{self.type_struct_mn}* nocapture %0, {args}) local_unnamed_addr #0 {{",
            ] + copies + [ 
                f"  ret void",
                f"}}",
            ]


@dataclass
class DefaultStructCopyPrimitive(Primitive):
    fn_mn: str
    type_struct_mn: str
    types_mn: List[str]
    copy_calls_mn: List[str]

    def get_code(self):
        n = len(self.types_mn)

        calls = []
        for i in range(n):
            calls.append(f"%t_{2*i} = getelementptr inbounds %{self.type_struct_mn}, %{self.type_struct_mn}* %dst, i64 0, i32 {i}")
            calls.append(f"%t_{2*i+1} = getelementptr inbounds %{self.type_struct_mn}, %{self.type_struct_mn}* %src, i64 0, i32 {i}")
            calls.append(f"call void @{self.copy_calls_mn[i]}(%{self.types_mn[i]}* %t_{2*i}, %{self.types_mn[i]}* %t_{2*i+1})")

        return [
                f"; Function Attrs: nofree norecurse nounwind sspstrong uwtable",
                f"define dso_local void @{self.fn_mn}(%{self.type_struct_mn}* nocapture %dst, %{self.type_struct_mn}* nocapture %src) local_unnamed_addr #0 {{",
            ] + calls + [ 
                f"  ret void",
                f"}}",
            ]

@dataclass
class DefaultStructDestPrimitive(Primitive):
    fn_mn: str
    type_struct_mn: str
    types_mn: List[str]
    dest_calls_mn: List[str]

    def get_code(self):
        n = len(self.types_mn)

        calls = []
        for i in range(n):
            calls.append(f"%t_{i} = getelementptr inbounds %{self.type_struct_mn}, %{self.type_struct_mn}* %todest, i64 0, i32 {i}")
            calls.append(f"call void @{self.dest_calls_mn[i]}(%{self.types_mn[i]}* %t_{i})")

        return [
                f"; Function Attrs: nofree norecurse nounwind sspstrong uwtable",
                f"define dso_local void @{self.fn_mn}(%{self.type_struct_mn}* nocapture %todest) local_unnamed_addr #0 {{",
            ] + calls + [ 
                f"  ret void",
                f"}}",
            ]

@dataclass
class DefaultBuiltinInitPrimitive(Primitive):
    fn_mn: str
    type_mn: str

    def get_code(self):
        return [
            f"define dso_local void @{self.fn_mn}(%{self.type_mn}* %0, %{self.type_mn} %1){{",
            f"store %{self.type_mn} %1, %{self.type_mn}* %0",
            f"ret void",
            f"}}",
        ]

@dataclass
class DefaultBuiltinCopyPrimitive(Primitive):
    fn_mn: str
    type_mn: str

    def get_code(self):
        return [
            f"define dso_local void @{self.fn_mn}(%{self.type_mn}* %0, %{self.type_mn}* %1){{",
            f"%val = load %{self.type_mn}, %{self.type_mn}* %1",
            f"store %{self.type_mn} %val, %{self.type_mn}* %0",
            f"ret void",
            f"}}",
        ]

@dataclass
class DefaultBuiltinDestPrimitive(Primitive):
    fn_mn: str
    types_mn: List[str]

    def get_code(self):
        n = len(self.types_mn)

        args = ", ".join([f"%{self.types_mn[i]} %t_{i}" for i in range(n)])


        return [
                f"; Function Attrs: nofree norecurse nounwind sspstrong uwtable",
                f"define dso_local void @{self.fn_mn}({args}) local_unnamed_addr #0 {{",
                f"  ret void",
                f"}}",
            ]

#
#
# INT/BOOL OPERATIONS PRIMITIVES
#
#




@dataclass
class InIntBoolPrimitive(Primitive):
    mangled_name: str
    size: int
    def get_code(self):
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

@dataclass
class OutIntBoolPrimitive(Primitive):
    mangled_name: str
    size: int
    def get_code(self):
        ext_mode = "sext" if self.size>1 else "zext"
        return [
            f"; Function Attrs: nofree nounwind sspstrong uwtable",
            f"define dso_local void @{self.mangled_name}(i{self.size} %0) local_unnamed_addr #0 {{",
            f"  %2 = {ext_mode} i{self.size} %0 to i64",
            f"  %3 = tail call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([5 x i8], [5 x i8]* @.out_int_str, i64 0, i64 0), i64 %2)",
            f"  ret void",
            f"}}",
        ]

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


