import sys
from typing import Dict, List, Tuple
from enum import Enum

from . import type_system as ts

from .recursive_logger import RecursiveLogger
from . import inference_errors as ierr
from .scope_manager import GlobalScopeManager


class TypingContext:
    def __init__(self, func_defs, struct_defs):
        self.func_defs = func_defs
        self.struct_defs = struct_defs

        self.scope_man = GlobalScopeManager()

        self.function_type_container: Dict[Tuple, ts.FunctionType] = dict()
        self.struct_type_container: Dict[Tuple, ts.Type] = dict()
        self.visited_resolve_methods: Set[Tuple] = set()

        self.code_blocks: List = []

        self.recursive_logger: RecursiveLogger = RecursiveLogger()

    def resolve_function(self, 
                            name: str,
                            type_argument_types: Tuple[ts.Type],
                            argument_types: Tuple[ts.Type]
                            ) -> ts.FunctionType:
        from . import type_gens
        desc = (
            name, 
            type_argument_types, 
            argument_types,
        )
        self.recursive_logger.go_in()
        self.recursive_logger.log(f"{desc} ???")

        # cache inspection and modificaiton

        if desc in self.function_type_container:
            f = self.function_type_container[desc]
            self.recursive_logger.log(f"{desc} -> {f}")
            self.recursive_logger.go_out()
            return f
        elif desc in self.visited_resolve_methods:
            self.recursive_logger.go_out()
            raise ierr.InferenceError(f"Can not infer function {desc} (already tried)!")
        self.visited_resolve_methods.add(desc)

        # function generators invocation

        candidates = []
        candidates_lower_prio = []

        for fm in type_gens.func_methods:
            try:
                res = fm(self, name, type_argument_types, argument_types)
                if isinstance(res, Tuple):
                    candidates_lower_prio.append(res[0])
                else:
                    candidates.append(res)
            except ierr.TypeGenError as e:
                pass

        # func definition resolution

        for fd in self.func_defs:
            fd: sa.FunctionDefinition
            if all([
                fd.name == name,
                len(fd.type_parameter_names) == len(type_argument_types),
                len(fd.parameter_names) == len(argument_types),
            ]):
                try:
                    r = fd.te_visit(self, type_argument_types, argument_types)
                    candidates.append(r)
                except ierr.ChoiceSkipError as cse:
                    pass

        # decision

        if len(candidates)==1:
            self.function_type_container[desc] = candidates[0]
            self.recursive_logger.log(f"{desc} -> {candidates[0]}")
            self.recursive_logger.go_out()
            return candidates[0]
        elif len(candidates)==0:
            if len(candidates_lower_prio)==1:
                self.function_type_container[desc] = candidates_lower_prio[0]
                self.recursive_logger.log(f"{desc} -> {candidates_lower_prio[0]}")
                self.recursive_logger.go_out()
                return candidates_lower_prio[0]
            elif len(candidates_lower_prio)==0:
                self.recursive_logger.go_out()
                raise ierr.InferenceError(f"Can not infer function {desc} (no candidates)!")
            else:
                self.recursive_logger.go_out()
                raise ierr.InferenceError(f"Can not infer function {desc} (too many DEFAULT candidates)!")
        else:
            self.recursive_logger.go_out()
            raise ierr.InferenceError(f"Can not infer function {desc} (too many candidates)!")


    def resolve_struct(self, 
                        name: str,
                        type_argument_types: Tuple[ts.Type],
                        ) -> ts.StructType:
        from . import type_gens
        desc = (
            name, 
            type_argument_types, 
        )
        self.recursive_logger.go_in()
        self.recursive_logger.log(f"{desc} ???")

        # cache inspection and modificaiton

        if desc in self.struct_type_container:
            s = self.struct_type_container[desc]
            self.recursive_logger.log(f"{desc} -> {s}")
            self.recursive_logger.go_out()
            return s
        elif desc in self.visited_resolve_methods:
            self.recursive_logger.go_out()
            raise ierr.InferenceError(f"Can not infer struct {desc} (already tried)!")
        self.visited_resolve_methods.add(desc)

        # struct generators invocation

        candidates = []

        for sm in type_gens.struct_methods:
            try:
                res = sm(self, name, type_argument_types)
                candidates.append(res)
            except ierr.TypeGenError as e:
                pass

        # struct definition resolution

        for sd in self.struct_defs:
            sd: sa.StructDefinition
            if all([
                sd.name == name,
                len(sd.type_parameter_names) == len(type_argument_types),
            ]):
                try:
                    r = sd.te_visit(self, type_argument_types)
                    candidates.append(r)
                except ierr.ChoiceSkipError as cse:
                    pass

        # decision

        if len(candidates)==1:
            self.struct_type_container[desc] = candidates[0]
            self.recursive_logger.log(f"{desc} -> {candidates[0]}")
            self.recursive_logger.go_out()
            return candidates[0]
        elif len(candidates)==0:
            self.recursive_logger.go_out()
            raise ierr.InferenceError(f"Can not infer struct {desc} (no candidates)!")
        else:
            self.recursive_logger.go_out()
            raise ierr.InferenceError(f"Can not infer struct {desc} (too many candidates)!")


class TypingResult:
    def __init__(self, tc: TypingContext):
        self.code_blocks = tc.code_blocks
        self.recursive_logger = tc.recursive_logger

        main_desc = ("main", (), ())
        if main_desc in tc.function_type_container:
            self.main_name = tc.function_type_container[main_desc].mangled_name
        else:
            self.main_name = None


def run(func_defs, struct_defs):
    tc = TypingContext(func_defs, struct_defs)
    m = tc.resolve_function("main", (), ())

    return TypingResult(tc)
