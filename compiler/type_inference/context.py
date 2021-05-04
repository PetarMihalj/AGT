from typing import Dict, List, Set
import ts

from .scope_manager import DefinitionScopeManager, GlobalScopeManager

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
    def __init__(self, mangled_name)
        self.mangled_name: str = mangled_name
        self.types: Dict[str, ts.Type] = {}
        self.members: List[str] = []
        self.return_type: ts.Type = return_type
        self.scope_man = DefinitionScopeManager()


class TypingContext:
    def __init__(self, func_defs, struct_defs):
        self.func_defs = func_defs
        self.struct_defs = struct_defs

        self.scope_man = GlobalScopeManager()

        self.function_type_container: Dict[Tuple, ts.FunctionType] = dict()
        self.struct_type_container: Dict[Tuple, ts.Type] = dict()

        self.visited_resolve_methods: Set[Tuple] = set()

        self.recursive_logger: RecursiveLogger = RecursiveLogger()
        self.primitives: List[Primitive] = []
