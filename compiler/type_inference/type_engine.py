import sys
from typing import Dict, List, Tuple
from enum import Enum

from . import primitives as prim
from ..helpers import tree_print
from . import type_system as ts
from .type_gens import gen_function, gen_struct

from ..semantics_parsing import semantic_ast as sa
from .recursive_logger import RecursiveLogger, LogTypes

separator = "_$_"

class ScopeManager:
    def __init__(self):
        self.scope_stack: List[dict[str]] = []
        self.dest_stack: List[List[str]] = []

        self.var_cnt = 0
        self.tmp_var_cnt = 0
        self.impl_var_cnt = 0

        self.label_cnt = 0
        self.func_cnt = 0
        self.struct_cnt = 0

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

    def new_tmp_var_name(self, description="", type_name=False):
        self.tmp_var_cnt += 1
        if type_name:
            res_var = f"tmp_type_var{description}{separator}{self.tmp_var_cnt}"
        else:
            res_var = f"tmp_var{description}{separator}{self.tmp_var_cnt}"

        return res_var

    def new_impl_var_name(self):
        self.impl_var_cnt += 1
        return f"impl_var{separator}{self.impl_var_cnt}"


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

        self.logger: RecursiveLogger = RecursiveLogger()
        self.gen_set = set()

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
        self.logger.go_in()
        self.logger.log(f"Resolving function {desc}", 
                LogTypes.FUNCTION_RESOLUTION)

        gen_function(self, name, type_argument_types, argument_types)
        if desc in self.function_type_container:
            self.logger.log(f"[SUCC] Resolving function {desc}", 
                    LogTypes.FUNCTION_RESOLUTION)
            self.logger.go_out()
            return self.function_type_container[desc]

        candidates = []
        for fd in self.func_defs:
            fd: sa.FunctionDefinition
            if all([
                fd.name == name,
                len(fd.type_parameter_names) == len(type_argument_types),
                len(fd.parameter_names) == len(argument_types),
            ]):
                r = fd.te_visit(self, 
                        type_argument_types, argument_types)
                if r is not None:
                    candidates.append(r)
        if len(candidates)==1:
            self.function_type_container[desc] = candidates[0]
            self.logger.log(f"[SUCC] Resolving function {desc}", 
                    LogTypes.FUNCTION_RESOLUTION)
            self.logger.go_out()
            return candidates[0]
        elif len(candidates)==0:
            self.logger.log(f"[FAIL] Resolving function {desc}", 
                    LogTypes.FUNCTION_RESOLUTION)
            self.logger.go_out()
            return None
        else:
            self.logger.log(f"[FAIL] Resolving function with too much {desc}", 
                    LogTypes.FUNCTION_RESOLUTION)
            self.logger.go_out()
            return None


    def resolve_struct(self, name: str,
                       type_argument_types: List[ts.Type],
                       use_gens = True)\
                -> ts.StructType:
        desc = (
            name, 
            tuple(type_argument_types), 
        )
        self.logger.go_in()
        self.logger.log(f"Resolving struct {desc}", 
                LogTypes.STRUCT_RESOLUTION)

        gen_struct(self, name, type_argument_types)
        if desc in self.struct_type_container:
            self.logger.log(f"[SUCC] Resolving struct {desc}", 
                    LogTypes.STRUCT_RESOLUTION)
            self.logger.go_out()
            return self.struct_type_container[desc]
        candidates = []
        for sd in self.struct_defs:
            sd: sa.StructDefinition
            if all([
                sd.name == name,
                len(sd.type_parameter_names) == len(type_argument_types),
            ]):
                r = sd.te_visit(self, type_argument_types)
                if r is not None:
                    candidates.append(r)
        if len(candidates)==1:
            self.struct_type_container[desc] = candidates[0]
            self.logger.log(f"[SUCC] Resolving struct {desc}", 
                    LogTypes.STRUCT_RESOLUTION)
            self.logger.go_out()
            return candidates[0]
        elif len(candidates)==0:
            self.logger.log(f"[FAIL] Resolving struct {desc}", 
                    LogTypes.STRUCT_RESOLUTION)
            self.logger.go_out()
            return None
        else:
            self.logger.log(f"[FAIL] Resolving struct {desc}", 
                    LogTypes.STRUCT_RESOLUTION)
            self.logger.go_out()
            return None
