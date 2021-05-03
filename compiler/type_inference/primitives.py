from dataclasses import dataclass
from typing import List
from . import TypingResult

class Primitive:
    pass

# 
#
# OBJECT CREATION PRIMITIVES
#
#

@dataclass
class HeapObjectPrimitive(Primitive):
    fn_mn: str
    type_struct_mn: str
    types_mn: List[str]

    alloc_fn_i32_mn: str
    init_fn_mn: str

    def get_code(self, tr: TypingResult):
        n = len(self.types_mn)

        args = ", ".join([f"%{self.types_mn[i]} %t_{i}" for i in range(n)])

        return [
                f"; Function Attrs: nofree norecurse nounwind sspstrong uwtable writeonly",
                f"define dso_local %{self.type_struct_mn}* @{self.fn_mn}({args}) local_unnamed_addr #0 {{",
                f"%ptr = call %{self.type_struct_mn}* @{self.alloc_fn_i32_mn}(i32 1)",
                f"call void @{self.init_fn_mn}(%{self.type_struct_mn}* %ptr, {args})",
                f"ret %{self.type_struct_mn}* %ptr",
                f"}}",
            ]

@dataclass
class StackObjectPrimitive(Primitive):
    fn_mn: str
    type_struct_mn: str
    types_mn: List[str]

    init_fn_mn: str

    def get_code(self, tr: TypingResult):
        n = len(self.types_mn)

        args = ", ".join([f"%{self.types_mn[i]} %t_{i}" for i in range(n)])

        return [
                f"; Function Attrs: nofree norecurse nounwind sspstrong uwtable writeonly",
                f"define dso_local %{self.type_struct_mn} @{self.fn_mn}({args}) local_unnamed_addr #0 {{",
                f"%ptr = alloca %{self.type_struct_mn}",
                f"call void @{self.init_fn_mn}(%{self.type_struct_mn}* %ptr, {args})",
                f"%item = load %{self.type_struct_mn}, %{self.type_struct_mn}* %ptr",
                f"ret %{self.type_struct_mn} %item",
                f"}}",
            ]

#
#
# HEAP MEMORY PRIMITIVES
#
#

@dataclass
class HeapAllocPrimitive(Primitive):
    mangled_name: str
    type_mangled_name: str
    size_type_mangled_name: str
    def get_code(self, tr: TypingResult):
        return [
            f"; Function Attrs: noinline nounwind optnone sspstrong uwtable",
            f"define dso_local %{self.type_mangled_name}* @{self.mangled_name}(%{self.size_type_mangled_name} %0) #0 {{",
            f"  %2 = alloca %{self.size_type_mangled_name}",
            f"  store %{self.size_type_mangled_name} %0, %{self.size_type_mangled_name}* %2",
            f"  %3 = load %{self.size_type_mangled_name}, %{self.size_type_mangled_name}* %2",
            f"  %4 = sext %{self.size_type_mangled_name} %3 to i64",
            "",
            f"  %Size = getelementptr %{self.type_mangled_name}, %{self.type_mangled_name}* null, i32 1",
            f"  %SizeI = ptrtoint %{self.type_mangled_name}* %Size to i64",
            "",
            f"  %5 = mul i64 %SizeI, %4",
            f"  %6 = call noalias i8* @malloc(i64 %5) #2",
            f"  %7 = bitcast i8* %6 to %{self.type_mangled_name}*",
            f"  ret %{self.type_mangled_name}* %7",
            f"}}",
        ]

@dataclass
class HeapFreePrimitive(Primitive):
    mangled_name: str
    type_mangled_name: str
    def get_code(self, tr: TypingResult):
        return [
            f"; Function Attrs: nounwind sspstrong uwtable",
            f"define dso_local void @{self.mangled_name}(%{self.type_mangled_name}* nocapture %0) local_unnamed_addr #0 {{",
            f"  %2 = bitcast %{self.type_mangled_name}* %0 to i8*",
            f"  tail call void @free(i8* %2) #2",
            f"  ret void",
            f"}}",
        ]

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

    def get_code(self, tr: TypingResult):
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

    def get_code(self, tr: TypingResult):
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

    def get_code(self, tr: TypingResult):
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

    def get_code(self, tr: TypingResult):
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

    def get_code(self, tr: TypingResult):
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

    def get_code(self, tr: TypingResult):
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
class CastIntBoolPrimitive(Primitive):
    mangled_name: str
    target_size: int
    source_size: int
    def get_code(self, tr: TypingResult):
        if self.target_size < self.source_size:
            return [
                f"; Function Attrs: norecurse nounwind readnone sspstrong uwtable",
                f"define dso_local i{self.target_size} @{self.mangled_name}(i{self.source_size} %0) local_unnamed_addr #0 {{",
                f"  %2 = trunc i{self.source_size} %0 to i{self.target_size}",
                f"  ret i{self.target_size} %2",
                f"}}",
            ]
        else:
            return [
                f"; Function Attrs: norecurse nounwind readnone sspstrong uwtable",
                f"define dso_local i{self.target_size} @{self.mangled_name}(i{self.source_size} %0) local_unnamed_addr #0 {{",
                f"  %2 = sext i{self.source_size} %0 to i{self.target_size}",
                f"  ret i{self.target_size} %2",
                f"}}",
            ]

@dataclass
class InIntBoolPrimitive(Primitive):
    mangled_name: str
    size: int
    def get_code(self, tr: TypingResult):
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
    def get_code(self, tr: TypingResult):
        return [
            f"; Function Attrs: nofree nounwind sspstrong uwtable",
            f"define dso_local void @{self.mangled_name}(i{self.size} %0) local_unnamed_addr #0 {{",
            f"  %2 = sext i{self.size} %0 to i64",
            f"  %3 = tail call i32 (i8*, ...) @printf(i8* nonnull dereferenceable(1) getelementptr inbounds ([6 x i8], [6 x i8]* @.out_int_str, i64 0, i64 0), i64 %2)",
            f"  ret void",
            f"}}",
        ]

@dataclass
class IntTypeOpPrimitive(Primitive):
    mangled_name: str
    op: str
    size: int

    def get_code(self, tr: TypingResult):
        def arithmetic(opname):
            return [
                f"define dso_local i{self.size} @{self.mangled_name}(i{self.size} %0, i{self.size} %1) {{",
                f"  %3 = {opname} nsw i{self.size} %0, %1",
                f"  ret i{self.size} %3",
                f"}}",
            ]
        def comp(opname):
            return [
                f"define dso_local i1 @{self.mangled_name}(i{self.size} %0, i{self.size} %1) {{",
                f"\t%3 = icmp {opname} i{self.size} %0, %1",
                f"\tret i1 %3",
                f"}}",
            ]

        mapping = {
                "__eq__": (comp, "eq"),
                "__ne__": (comp, "ne"),
                '__gt__': (comp, "sgt"),
                '__lt__': (comp, "slt"),
                '__le__': (comp, "sle"),
                '__ge__': (comp, "sge"),

                '__add__': (arithmetic, "add"),
                '__sub__': (arithmetic, "sub"),
                '__mul__': (arithmetic, "mul"),
                '__div__': (arithmetic, "sdiv"),
                '__mod__': (arithmetic, "srem"),
        }

        f,opname = mapping[self.op]
        return f(opname)


@dataclass
class TypeToValuePrimitive(Primitive):
    mangled_name: str
    value: int
    size: int

    def get_code(self, tr: TypingResult):
        return [
            f"define dso_local i{self.size} @{self.mangled_name}() #0 {{",
            f"  ret i{self.size} {self.value}",
            f"}}",
        ]
