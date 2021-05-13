from . import type_system
from . import inference_errors
from . import recursive_logger
from . import scope_manager

from . import context

from . import code_blocks

from . import flat_ir

from . import type_engine
from . import type_engine_rules
from . import type_gens

from . import generator

def get_code(semantics_ast):
    try:
        tr: type_engine.TypingResult = type_engine.run(
            semantics_ast.function_definitions,
            semantics_ast.struct_definitions,
        )
    except inference_errors.InferenceError as e:
        print("Can not compile the program because of errors!")
        print()
        stack = [e]
        while e.__cause__ is not None:
            stack.append(e.__cause__)
            e = e.__cause__

        for i, e in enumerate(stack):
            print(f"{i}: {e}")

        exit(1)


    cg = generator.CodeGenerator(tr)
    cg.run()
    return cg.code

