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
class HeapFreePrimitive(Primitive):
    type_mangled_name: str
    size_type_mangled_name: str

@dataclass
class CastPrimitive(Primitive):
    type_target_mangled_name: str
    type_source_mangled_name: str

@dataclass
class InInt32Primitive(Primitive):
    pass

@dataclass
class OutInt32Primitive(Primitive):
    pass
