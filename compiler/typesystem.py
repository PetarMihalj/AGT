from dataclasses import dataclass
from typing import List, Tuple
import unifier as u


class Type:
    pass


@dataclass
class IntType(Type):
    width: int
    signed: bool


@dataclass
class BoolType(Type):
    pass


@dataclass
class VoidType(Type):
    pass


@dataclass
class FunctionType(Type):
    name: str
    parameter_types: List[Type]
    return_type: Type


@dataclass
class StructType(Type):
    name: str
    template_parameters: List[Tuple[str, Type]]
    members: List[Tuple[str, Type]]


def unify_struct(call: Type, struct: Type):
    pass
