from . import type_engine
from . import type_system
from . import type_engine_rules
from . import type_gens

def get_typed_program(semantics_ast):
    from .type_engine import TypingContext
    tr: type_engine.TypingResult = type_engine.run(
            semantics_ast.function_definitions,
            semantics_ast.struct_definitions,
    )
    return tr





