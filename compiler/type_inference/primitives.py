from dataclasses import dataclass
from . import TypingResult

class Primitive:
    pass

@dataclass
class IntTypePrimitive(Primitive):
    mangled_name: str
    size: int

    def get_code(self, tr: TypingResult):
        return [
            f"%{self.mangled_name} = type i{self.size}",
        ]

@dataclass
class BoolTypePrimitive(Primitive):
    mangled_name: str

    def get_code(self, tr: TypingResult):
        return [
            f"%{self.mangled_name} = type i1",
        ]

@dataclass
class MemoryCopyPrimitive(Primitive):
    fn_mn: str
    type_mn: str

    def get_code(self, tr: TypingResult):
        return [
            f"define dso_local void @{self.fn_mn}(%{self.type_mn}* %0, %{self.type_mn}* %1){{",
            f"%val = load {self.type_mn}, {self.type_mn}* %1",
            f"store {self.type_mn} %val, {self.type_mn}* %0",
            f"ret void",
            f"}}",
        ]

@dataclass
class MemoryInitPrimitive(Primitive):
    fn_mn: str
    type_mn: str

    def get_code(self, tr: TypingResult):
        return [
            f"define dso_local void @{self.fn_mn}(%{self.type_mn}* %0, %{self.type_mn} %1){{",
            f"store {self.type_mn} %1, {self.type_mn}* %0",
            f"ret void",
            f"}}",
        ]

@dataclass
class HeapAllocPrimitive(Primitive):
    mangled_name: str
    type_mangled_name: str
    size_type_mangled_name: str
    def get_code(self, tr: TypingResult):
        return [
            "; Function Attrs: nounwind",
            "declare noalias i8* @malloc(i64) #1",
            "",
            "",
            "; Function Attrs: noinline nounwind optnone sspstrong uwtable",
            f"define dso_local %{self.type_mangled_name}* @{self.mangled_name}({self.size_type_mangled_name} %0) #0 {{",
            f"  %2 = alloca %{self.size_type_mangled_name}",
            f"  store %{self.size_type_mangled_name} %0, %{self.size_type_mangled_name}* %2",
            f"  %3 = load %{self.size_type_mangled_name}, %{self.size_type_mangled_name}* %2",
            f"  %4 = sext %{self.size_type_mangled_name} %3 to i64",
            f"  %Size = getelementptr %{self.size_type_mangled_name}* null, i32 1",
            f"  %SizeI = ptrtoint %{self.size_type_mangled_name}* %Size to i64",
            "  %5 = mul %SizeI, %4",
            "  %6 = call noalias i8* @malloc(i64 %5) #2",
            f"  %7 = bitcast i8* %6 to %{self.type_mangled_name}*",
            f"  ret %{self.type_mangled_name}* %7",
            "}",
        ]

@dataclass
class HeapFreePrimitive(Primitive):
    mangled_name: str
    type_mangled_name: str
    size_type_mangled_name: str
    def get_code(self, tr: TypingResult):
        return []

@dataclass
class CastPrimitive(Primitive):
    mangled_name: str
    type_target_mangled_name: str
    type_source_mangled_name: str
    def get_code(self, tr: TypingResult):
        return []

@dataclass
class InInt32Primitive(Primitive):
    mangled_name: str
    def get_code(self, tr: TypingResult):
        return []

@dataclass
class OutInt32Primitive(Primitive):
    mangled_name: str
    def get_code(self, tr: TypingResult):
        return []

@dataclass
class IntTypeOp(Primitive):
    mangled_name: str
    op: str
    size: int

    def get_code(self, tr: TypingResult):
        def arithmetic(opname):
            return [
                f"define dso_local i{self.size} @{self.mangled_name}(i{self.size} %0, i{self.size} %1) {{",
                f"  %3 = {opname} nsw i{self.size} %1, %0",
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













