from . import type_system
from . import inference_errors
from . import recursive_logger
from . import scope_manager

from . import context

from . import code_blocks
from . import primitives

from . import flat_ir

from . import type_engine
from . import type_engine_rules
from . import type_gens

def get_typed_program(semantics_ast):
    tr: type_engine.TypingResult = type_engine.run(
        semantics_ast.function_definitions,
        semantics_ast.struct_definitions,
    )
    return tr





