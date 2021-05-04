from typing import Dict, List, Set

from . import type_system as ts
from .scope_manager import DefinitionScopeManager, GlobalScopeManager
from .recursive_logger import RecursiveLogger

class FunctionContext:
    def __init__(self, mangled_name):
        self.mangled_name: str = mangled_name

        self.parameter_names_ordered: List[str] = []
        self.types: Dict[str, ts.Type] = {}

        self.return_type = None

        self.code: List[str] = []

        self.dest_stack: List[List[str]] = []
        self.break_label_stack = []

        self.scope_man = DefinitionScopeManager()


class StructContext:
    def __init__(self, mangled_name):
        self.mangled_name: str = mangled_name
        self.types: Dict[str, ts.Type] = {}
        self.members: List[str] = []
        self.return_type: ts.Type = None


