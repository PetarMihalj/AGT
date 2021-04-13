from syntactic_ast import compile_syntactic_ast
from semantic_ast import compile_semantic_ast
from helpers import tree_print
import sys
from typing import Dict, List
import type_system as ts
import semantic_ast as sa
from type_engine_rules import NoInferencePossibleError


separator = "_$_"


class ScopeManager:
    def __init__(self):
        self.scope_stack: List[dict[str]] = []
        self.label_cnt = 0
        self.tmp_var_cnt = 0
        self.var_cnt = 0
        self.func_cnt = 0
        self.struct_cnt = 0
        self.break_label_stack = []

    def begin_scope(self):
        self.scope_stack.append(dict())

    def end_scope(self):
        self.scope_stack.pop()

    # var names

    def new_var_name(self, name, type_name=False):
        self.var_cnt += 1
        if type_name:
            res_var = f"t_var{separator}{name}{separator}{self.var_cnt}"
        else:
            res_var = f"var{separator}{name}{separator}{self.var_cnt}"
        self.scope_stack[-1][name] = res_var
        return res_var

    def get_var_name(self, name: str):
        for s in reversed(self.scope_stack):
            if name in s:
                return s[name]

    # label names

    def new_label_name(self, description=""):
        self.label_cnt += 1
        return f"label{description}{separator}{self.label_cnt}"

    # tmp var names

    def new_tmp_var_name(self, description=""):
        self.tmp_var_cnt += 1
        return f"tmp_var{description}{separator}{self.tmp_var_cnt}"

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
        self.function_type_container = dict()
        self.struct_type_container = dict()

    def resolve_function(self, name: str,
                         type_argument_types: List[ts.Type],
                         argument_types: List[ts.Type]):
        desc = (
            name, 
            type_argument_types, 
            argument_types
        )
        if desc in self.function_type_container:
            return desc
        candidates = []
        for fd in self.func_defs:
            fd: sa.FunctionDefinition
            if all([
                fd.name == name,
                len(fd.type_parameter_names) == type_argument_types,
                len(fd.parameter_names) == argument_types,
            ]):
                try:
                    r = fd.te_visit(tc, type_argument_types, args)
                    candidates.append(r)
                except...:
                    pass
        if len(candidates)==1:
            self.function_type_container[desc] = candidates[0]
            return candidates[0]
        elif len(candidates)==0:
            raise NoInferencePossibleError("cant synth")
        else:
            raise NoInferencePossibleError("multiple synth")

    def resolve_struct(self, name: str,
                       type_argument_types: List[ts.Type]):
        desc = (
            name, 
            type_argument_types, 
        )
        if desc in self.struct_type_container:
            return desc
        candidates = []
        for sd in self.struct_defs:
            sd: sa.StructDefinition
            if all([
                sd.name == name,
                len(sd.type_parameter_names) == type_argument_types,
            ]):
                try:
                    r = sd.te_visit(tc, type_argument_types, args)
                    candidates.append(r)
                except...:
                    pass
        if len(candidates)==1:
            self.struct_type_container[desc] = candidates[0]
            return candidates[0]
        elif len(candidates)==0:
            raise NoInferencePossibleError("cant synth")
        else:
            raise NoInferencePossibleError("multiple synth")


def compile_types(sem_ast):
    tc = TypingContext(sem_ast.function_definitions,
                       sem_ast.struct_definitions)
    tc.resolve_function(tc, "main", [], [])
    return tc


if __name__ == '__main__':
    data = open(sys.argv[1]).read()
    syn_ast = compile_syntactic_ast(data)
    sem_ast = compile_semantic_ast(syn_ast)
    tc = compile_types(sem_ast)
    print(tc)
