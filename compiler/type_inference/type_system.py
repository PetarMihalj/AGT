from typing import Dict, List, Set
import re
from dataclasses import dataclass
from enum import Enum

class Type:
    pass

class BoolType(Type):
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



class VoidType(Type):
    def __init__(self):
        self.mangled_name = "void"

    def __eq__(self, other):
        if not isinstance(other, VoidType):
            return False
        return True

    def __hash__(self):
        return hash(self.mangled_name)
    def __repr__(self):
        return type(self).__name__


class IntType(Type):
    def __init__(self, size):
        self.size = size
        self.mangled_name = f"i{size}"

    def __eq__(self, other):
        if not isinstance(other, IntType):
            return False
        return self.size == other.size

    def __hash__(self):
        return hash(self.mangled_name)

    def __repr__(self):
        return type(self).__name__


class FunctionType(Type):
    def __init__(self, name):
        self.name: str = name
        self.mangled_name: str = None

        self.break_label_stack = []

        self.parameter_names_ordered = List[str]

        self.types: Dict[str, Type] = {}
        self.flat_statements: List = []


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

    def __hash__(self):
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

