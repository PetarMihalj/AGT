from dataclasses import dataclass

class Primitive:
    pass

@dataclass
class IntTypePrimitive(Primitive):
    size: int

@dataclass
class VoidTypePrimitive(Primitive):
    pass

@dataclass
class VoidTypePrimitive(Primitive):
    pass

@dataclass
class HeapAllocPrimitive(Primitive):
    type_mangled_name: str
    size_type_mangled_name: str

@dataclass
class CastPrimitive(Primitive):
    type_target_mangled_name: str
    type_source_mangled_name: str

@dataclass
class InPrimitive(Primitive):
    pass

@dataclass
class OutPrimitive(Primitive):
    pass
