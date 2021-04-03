from lexer import Lexer
from parser import Parser
from helpers import tree_print
from typing import List, Tuple
from copy import deepcopy
import parser_rules as pr

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

    def get_var_name(self, name: str):
        for s in reversed(self.scope_stack):
            if name in s:
                return s[name]

    def new_label_name(self, description=""):
        self.label_cnt += 1
        return f"label{description}{separator}{self.label_cnt}"

    def new_tmp_var_name(self, description=""):
        self.tmp_var_cnt += 1
        return f"tmp_var{description}{separator}{self.tmp_var_cnt}"

    def new_var_name(self, name):
        self.var_cnt += 1
        res_var = f"var{separator}{name}{separator}{self.var_cnt}"
        self.scope_stack[-1][name] = res_var
        return res_var

    def new_func_name(self, name):
        self.func_cnt += 1
        res_var = f"func{separator}{name}{separator}{self.func_cnt}"
        return res_var

    def new_struct_name(self, name):
        self.struct_cnt += 1
        res_var = f"struct{separator}{name}{separator}{self.struct_cnt}"
        return res_var


class Resolver:
    def __init__(self, tree):
        self.sm = ScopeManager()

        # name -> def
        self.func = dict()
        self.struct = dict()

        self.funcNormal = [
            d for d in tree.definitionList
            if isinstance(d, pr.FunctionDefinition)
            and len(d.typeParameterList) == 0]
        self.structNormal = [
            d for d in tree.definitionList
            if isinstance(d, pr.StructDefinition)
            and len(d.typeParameterList) == 0]

        self.funcTemp = [
            d for d in tree.definitionList
            if isinstance(d, pr.FunctionDefinition)
            and len(d.typeParameterList) != 0]
        self.structTemp = [
            d for d in tree.definitionList
            if isinstance(d, pr.StructDefinition)
            and len(d.typeParameterList) != 0]

    def resolve_struct(self, name: str, template_arg_types: List[pr.Type]):
        if len(template_arg_types) == 0:
            for k, d in self.struct:
                fits, _ = self._struct_fits(d, name,
                                            template_arg_types)
                if fits:
                    return k
            for d in self.structNormal:
                fits, subs = self._struct_fits(d, name,
                                               template_arg_types)
                if fits:
                    n = self.sm.new_struct_name(name)
                    self.struct[n] = deepcopy(d)
                    self.struct[n].name = n
                    self.struct[n].type(self, subs)
                    return n
            return None
        else:
            pass

    def resolve_func(self, name: str, arg_types: List[pr.Type],
                     template_arg_types: List[pr.Type]):
        if len(template_arg_types) == 0:
            for k, d in self.func:
                fits, _ = self._func_fits(d, name,
                                          arg_types, template_arg_types)
                if fits:
                    return k
            for d in self.funcNormal:
                fits, subs = self._func_fits(d, name,
                                             arg_types, template_arg_types)
                if fits:
                    n = self.sm.new_func_name(name)
                    self.func[n] = deepcopy(d)
                    self.func[n].name = n
                    self.func[n].type(self, subs)
                    return n
            return None
        else:
            pass

    def _struct_fits(self, d, name: str,
                     template_arg_types: List[pr.Type]) -> Tuple[bool, dict]:
        if len(template_arg_types) == 0:
            if d.name == name:
                return [True, {}]
        else:
            every_fitting = []
            subs = {}
            for type 



            return [False, {}]

    def _func_fits(self, d, name: str, arg_types: List[pr.Type],
                   template_arg_types: List[pr.Type]) -> Tuple[bool, dict]:
        if len(template_arg_types) == 0:
            if d.name == name:
                if len(arg_types) == len(d.parameterList):
                    if all([
                        arg == param.type for arg, param in
                        zip(d.parameterList, arg_types)
                    ]):
                        return [True, {}]
        else:
            return [False, {}]


if __name__ == '__main__':
    data = open('prog1.st').read()
    lexer = Lexer()
    lexer.test(data)
    parser = Parser(lexer, debug=True)
    a = parser.parse(data)
    tree_print(a)
