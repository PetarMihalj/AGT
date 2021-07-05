from typing import Dict, List, Set
import re
from dataclasses import dataclass
from enum import Enum

class Type:
    pass

class ConcreteType:
    pass

class CharType(ConcreteType):
    def __init__(self):
        self.mangled_name = "char"

    def __eq__(self, other):
        if not isinstance(other, CharType):
            return False
        return True
    def __hash__(self):
        return hash(self.mangled_name)
    def __repr__(self):
        return type(self).__name__

class BoolType(ConcreteType):
    def __init__(self):
        self.mangled_name = "bool"

    def __eq__(self, other):
        if not isinstance(other, BoolType):
            return False
        return True

    def __hash__(self):
        return hash(self.mangled_name)
    def __repr__(self):
        return type(self).__name__

class IntType(ConcreteType):
    def __init__(self, size):
        self.mangled_name = f"i{size}"
        self.size = size

    def __eq__(self, other):
        if not isinstance(other, IntType):
            return False
        return self.size == other.size

    def __hash__(self):
        return hash(self.mangled_name)

    def __repr__(self):
        return f"{type(self).__name__}({self.size})"

class PointerType(ConcreteType):
    def __init__(self, pointed):
        self.pointed: Type = pointed
        self.mangled_name = f"{pointed.mangled_name}*"
    def __eq__(self, other):
        if not isinstance(other, PointerType):
            return False
        return self.pointed == other.pointed
    def __hash__(self):
        return hash(self.pointed)+1
    def __repr__(self):
        return f"PointerType({self.pointed})"

class StructType(ConcreteType):
    def __init__(self, mangled_name, types: Dict[str,Type], members: List[str], return_type: Type):
        self.mangled_name: str = mangled_name
        self.types: Dict[str, Type] = types
        self.members: List[str] = members
        self.return_type: Type = return_type

    def __eq__(self, other):
        if not isinstance(other, StructType):
            return False
        return self.mangled_name == other.mangled_name

    def __hash__(self):
        return hash(self.mangled_name)
    def __repr__(self):
        return f"StructType({self.mangled_name})"

class FunctionType(Type):
    def __init__(self, name: str, retty: Type, do_not_copy_args: bool):
        self.mangled_name: str = name
        self.return_type: Type = retty

        self.do_not_copy_args: bool = do_not_copy_args

    def __repr__(self):
        return f"FuncType({self.mangled_name})"

    def __hash__(self):
        return hash(self.mangled_name)
