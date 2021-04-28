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
            f"%{self.mangled_name} = i{self.size}",
        ]

@dataclass
class VoidTypePrimitive(Primitive):
    mangled_name: str

    def get_code(self, tr: TypingResult):
        return [
            f"%{self.mangled_name} = void",
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
        return []
