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
        return []

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
