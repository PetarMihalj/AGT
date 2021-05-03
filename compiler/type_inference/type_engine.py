import sys
from typing import Dict, List, Tuple
from enum import Enum

from . import primitives as prim
from ..helpers import tree_print
from . import type_system as ts
from . import type_gens

from ..semantics_parsing import semantic_ast as sa
from .recursive_logger import RecursiveLogger

from . import inference_errors as ierr

separator = "$"

class ScopeManager:
    def __init__(self):
        self.scope_stack: List[dict[str]] = []
        self.dest_stack: List[List[str]] = []

        self.var_cnt = 0
        self.tmp_var_cnt = 0
        self.label_cnt = 0

        self.func_cnt = 0
        self.struct_cnt = 0

    def clear(self, no):
        while len(self.scope_stack)>no:
            self.scope_stack.pop()
        while len(self.dest_stack)>no:
            self.dest_stack.pop()

    def get_size(self):
        return len(self.scope_stack)

    def begin_scope(self):
        self.scope_stack.append(dict())
        self.dest_stack.append(list())

    def end_scope(self):
        self.scope_stack.pop()
        self.dest_stack.pop()

    def get_dest_list(self):
        return list(self.dest_stack[-1])

    def add_to_dest(self, name):
        self.dest_stack[-1].append(name)

    # var names

    def new_var_name(self, name, type_name=False):
        if name in self.scope_stack:
            return None
        
        self.var_cnt += 1
        if type_name:
            res_var = f"type_var{separator}{name}{separator}{self.var_cnt}"
        else:
            res_var = f"var{separator}{name}{separator}{self.var_cnt}"
        if name in self.scope_stack[-1]:
            raise RuntimeError(f"Cant override var name {name}, quitting")
        self.scope_stack[-1][name] = res_var
        return res_var

    def get_var_name(self, name: str):
        for s in reversed(self.scope_stack):
            if name in s:
                return s[name]
        return None

    def new_tmp_var_name(self, description="", type_name=False):
        self.tmp_var_cnt += 1
        if type_name:
            res_var = f"tmp_type_var{description}{separator}{self.tmp_var_cnt}"
        else:
            res_var = f"tmp_var{description}{separator}{self.tmp_var_cnt}"

        return res_var

    # label names

    def new_label_name(self, description=""):
        self.label_cnt += 1
        return f"label{description}{separator}{self.label_cnt}"

    def new_func_name(self, name):
        self.func_cnt += 1
        res_var = f"func{separator}{name}{separator}{self.func_cnt}"
        return res_var

    def new_struct_name(self, name):
        self.struct_cnt += 1
        res_var = f"struct{separator}{name}{separator}{self.struct_cnt}"
        return res_var


class TypingContext:
    def __init__(self, func_defs, struct_defs):
        self.func_defs = func_defs
        self.struct_defs = struct_defs

        self.scope_man = ScopeManager()
        self.function_type_container: Dict[Tuple, ts.FunctionType] = dict()
        self.struct_type_container: Dict[Tuple, ts.Type] = dict()

        self.recursive_logger: RecursiveLogger = RecursiveLogger()
        self.primitives: List[Primitive] = []

    def run(self):
        self.resolve_function("main", [], [])

        self.struct_type_container = dict([(k,s) for k,s in self.struct_type_container.items()\
            if isinstance(s,ts.StructType) and s.needs_gen])


    def resolve_function(self, name: str,
                         type_argument_types: List[ts.Type],
                         argument_types: List[ts.Type])\
                -> ts.FunctionType:
        desc = (
            name, 
            tuple(type_argument_types), 
            tuple(argument_types)
        )
        self.recursive_logger.go_in()

        # cache inspection

        if desc in self.function_type_container:
            f = self.function_type_container[desc]
            if f is None:
                raise ierr.InferenceError(f"Can not infer function {desc} (no or too many candidates)!")
            else:
                self.recursive_logger.log(f"{desc} -> {f}")
                return f

        # function generators invocation

        candidates = []
        for fm in type_gens.func_methods:
            try:
                res = fm(self, name, type_argument_types, argument_types)
                candidates.append(res)
            except ierr.InferenceError as e:
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
                    r = fd.te_visit(self, 
                            type_argument_types, argument_types)
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
            self.function_type_container[desc] = None
            self.recursive_logger.go_out()
            raise ierr.InferenceError(f"Can not infer function {desc} (no candidates)!")
        else:
            self.function_type_container[desc] = None
            self.recursive_logger.go_out()
            raise ierr.InferenceError(f"Can not infer function {desc} (too many candidates)!")


    def resolve_struct(self, name: str,
                       type_argument_types: List[ts.Type],
                       use_gens = True)\
                -> ts.StructType:
        desc = (
            name, 
            tuple(type_argument_types), 
        )
        self.recursive_logger.go_in()

        # cache inspection

        if desc in self.struct_type_container:
            s = self.struct_type_container[desc]
            if s is None:
                raise ierr.InferenceError(f"Can not infer struct {desc} (no or too many candidates)!")
            else:
                self.recursive_logger.log(f"{desc} -> {s}")
                return s

        # struct generators invocation

        candidates = []
        for sm in type_gens.struct_methods:
            try:
                res = sm(self, name, type_argument_types)
                candidates.append(res)
            except ierr.InferenceError as e:
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
            self.struct_type_container[desc] = None
            self.recursive_logger.go_out()
            raise ierr.InferenceError(f"Can not infer struct {desc} (no candidates)!")
        else:
            self.struct_type_container[desc] = None
            self.recursive_logger.go_out()
            raise ierr.InferenceError(f"Can not infer struct {desc} (too many candidates)!")
