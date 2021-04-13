from typing import Dict, List, Set
import flat_ir as ir
import re


class SyntError(BaseException):
    pass


class NoInferencePossibleError(BaseException):
    pass

#

class Type:
    pass


class BoolType(Type):
    pass


class VoidType(Type):
    pass


class IntType(Type):
    def __init__(self, size):
        self.size: int = size
    def __repr__(self):
        return f"IntType({self.size})"


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

class PointerType(Type):
    def __init__(self, pointed):
        self.pointed: Type = pointed

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
    

