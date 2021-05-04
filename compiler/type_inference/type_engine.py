import sys
from typing import Dict, List, Tuple
from enum import Enum

from . import primitives as prim
from . import type_system as ts
from . import type_gens

from .recursive_logger import RecursiveLogger
from . import inference_errors as ierr
from .context import TypingContext


def resolve_function(tc: TypingContext, 
                        name: str,
                        type_argument_types: Tuple[ts.Type],
                        argument_types: Tuple[ts.Type]
                        ) -> ts.FunctionType:
    desc = (
        name, 
        type_argument_types, 
        argument_types,
    )
    tc.recursive_logger.go_in()

    # cache inspection and modificaiton

    if desc in tc.function_type_container:
        f = tc.function_type_container[desc]
        tc.recursive_logger.log(f"{desc} -> {f}")
        return f
    elif desc in tc.visited_resolve_methods:
        raise ierr.InferenceError(f"Can not infer function {desc} (already tried)!")
    tc.visited_resolve_methods.append(desc)

    # function generators invocation

    candidates = []

    for fm in type_gens.func_methods:
        try:
            res = fm(tc, name, type_argument_types, argument_types)
            candidates.append(res)
        except ierr.TypeGenError as e:
            pass

    # func definition resolution

    for fd in tc.func_defs:
        fd: sa.FunctionDefinition
        if all([
            fd.name == name,
            len(fd.type_parameter_names) == len(type_argument_types),
            len(fd.parameter_names) == len(argument_types),
        ]):
            try:
                r = fd.te_visit(tc, 
                        type_argument_types, argument_types)
                candidates.append(r)
            except ierr.ChoiceSkipError as cse:
                pass

    # decision

    if len(candidates)==1:
        tc.function_type_container[desc] = candidates[0]
        tc.recursive_logger.log(f"{desc} -> {candidates[0]}")
        tc.recursive_logger.go_out()
        return candidates[0]
    elif len(candidates)==0:
        tc.recursive_logger.go_out()
        raise ierr.InferenceError(f"Can not infer function {desc} (no candidates)!")
    else:
        tc.recursive_logger.go_out()
        raise ierr.InferenceError(f"Can not infer function {desc} (too many candidates)!")


def resolve_struct(tc: TypingContext, 
                    name: str,
                    type_argument_types: Tuple[ts.Type],
                    ) -> ts.StructType:
    desc = (
        name, 
        type_argument_types, 
    )
    tc.recursive_logger.go_in()

    # cache inspection and modificaiton

    if desc in tc.struct_type_container:
        s = tc.struct_type_container[desc]
        tc.recursive_logger.log(f"{desc} -> {s}")
        return s
    elif desc in tc.visited_resolve_methods:
        raise ierr.InferenceError(f"Can not infer struct {desc} (already tried)!")
    tc.visited_resolve_methods.append(desc)

    # struct generators invocation

    candidates = []

    for sm in type_gens.struct_methods:
        try:
            res = sm(tc, name, type_argument_types)
            candidates.append(res)
        except ierr.TypeGenError as e:
            pass

    # struct definition resolution

    for sd in tc.struct_defs:
        sd: sa.StructDefinition
        if all([
            sd.name == name,
            len(sd.type_parameter_names) == len(type_argument_types),
        ]):
            try:
                r = sd.te_visit(tc, type_argument_types)
                candidates.append(r)
            except ierr.ChoiceSkipError as cse:
                pass

    # decision

    if len(candidates)==1:
        tc.struct_type_container[desc] = candidates[0]
        tc.recursive_logger.log(f"{desc} -> {candidates[0]}")
        tc.recursive_logger.go_out()
        return candidates[0]
    elif len(candidates)==0:
        tc.recursive_logger.go_out()
        raise ierr.InferenceError(f"Can not infer struct {desc} (no candidates)!")
    else:
        tc.recursive_logger.go_out()
        raise ierr.InferenceError(f"Can not infer struct {desc} (too many candidates)!")


class TypingResult:
    def __init__(self, func_types, struct_types, primitives, success, logger):
        self.func_types = func_types
        self.struct_types = struct_types
        self.primitives = primitives
        self.success = success
        self.logger = logger


def run(func_defs, struct_defs):
    tc = TypingContext(func_defs, struct_defs)
    m = resolve_function("main", (), ())

    return TypingResult(
        tc.function_type_container,
        tc.struct_type_container,
        tc.primitives
        tc.recursive_logger
    )
