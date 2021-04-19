from typing import Dict, List, Set
import flat_ir as ir
import re
from dataclasses import dataclass
from enum import Enum

#
class LogTypes(Enum):
    FUNCTION_RESOLUTION = 1
    STRUCT_RESOLUTION = 2

    FUNCTION_DEFINITION = 3
    STRUCT_DEFINITION = 4

    FUNCTION_OR_STRUCT_DEFINITION = 5

    TYPE_MISSMATCH = 6
    STATEMENT_ERROR = 7
    RUNTIME_EXPR_ERROR = 8

#
class Type:
    pass


@dataclass(unsafe_hash=True)
class BoolType(Type):
    pass 

@dataclass(unsafe_hash=True)
class VoidType(Type):
    pass

@dataclass(unsafe_hash=True)
class IntType(Type):
    size: int


class FunctionType(Type):
    def __init__(self, name):
        self.name: str = name
        self.mangled_name: str = None

        self.break_label_stack = []

        # this is important for runtime purposes
        self.parameter_names_ordered = List[str]

        self.types: Dict[str, Type] = {}
        self.flat_statements: List[ir.FlatStatement] = []



class StructType(Type):
    def __init__(self, name):
        self.name: str = name
        self.mangled_name: str = None

        self.types: Dict[str, Type] = {}
        self.members: Set[str] = set()

    def __eq__(self, other):
        if not isinstance(other, StructType):
            return False
        return self.mangled_name == other.mangled_name

    def __hash__(self, other):
        return hash(self.mangled_name)


class PointerType(Type):
    def __init__(self, pointed):
        self.pointed: Type = pointed
    def __eq__(self, other):
        if not isinstance(other, PointerType):
            return False
        return self.pointed == other.pointed
    def __hash__(self):
        return hash(self.pointed)+1

# -----


def match_and_ret(s: str, p: str):
    r = re.compile(p)
    m = r.match(s)
    if m is None:
        return None
    else:
        return m.group()


"""
def smt_bool(t: TypeExpression):
    if not isinstance(t, la.TypeExpressionGetStruct):
        return None
    t: la.TypeExpressionGetStruct
    if len(t.typeParameters) > 0:
        return None

    m = match_and_ret(t.name, r'bool|boolean')
    if m is None:
        return None
    return BoolType()


def smt_int(t: la.TypeExpression):
    if not isinstance(t, la.TypeExpressionGetStruct):
        return None
    t: pr.TypeExpressionGetStruct
    if len(t.typeParameters) > 0:
        return None

    m = match_and_ret(t.name, r'i([0-9]+)')
    if m is None:
        return None
    return IntType(m.group(1), True)
    """
    

