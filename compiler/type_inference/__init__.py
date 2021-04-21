from . import type_engine
from . import type_system
from . import type_engine_rules
from . import type_gens

class TypingResult:
    def __init__(self, func_types, struct_types, primitives, logger):
        self.func_types = func_types
        self.struct_types = struct_types
        self.primitives = primitives
        self.logger = logger


def get_typed_program(semantics_ast):
    from .type_engine import TypingContext
    tc = TypingContext(semantics_ast.function_definitions,
                       semantics_ast.struct_definitions,
                       )
    tc.run()
    return TypingResult(tc.function_type_container, 
            tc.struct_type_container, 
            tc.primitives,
            tc.logger)




