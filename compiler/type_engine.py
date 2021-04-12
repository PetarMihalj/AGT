from helpers import tree_print
import parser_rules
from parser import SyntaxParser, parse_semantics
from lexer import Lexer
import sys
from typing import Dict, List, Union
import lang_ast as la
from lang_ast import TypeExpression
import type_system as ts


# scope manager


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


class TypeExprEval:
    def __init__(self, resolution_methods):
        self.dict: Dict[TypeExpression, ts.Type] = {}
        self.resolution_methods = resolution_methods

    def __getitem__(self, te: TypeExpression):
        for m in self.resolution_methods:
            res = m(te)
            if res is not None:
                return res
        if te in self.dict:
            return self.dict[te]
        return None


class TypeEngine:
    def __init__(self, defs):
        self.scope_man = ScopeManager()
        self.func_eval = TypeExprEval(ts.func_resol_methods)
        self.struct_eval = TypeExprEval(ts.struct_resol_methods)


if __name__ == '__main__':
    data = open(sys.argv[1]).read()
    lexer = Lexer()
    lexer.test(data)

    parser = SyntaxParser(lexer, debug=False)
    s = parser.parse_syntax(data)
    tree_print(s)

    print("\n"*3)

    a = parse_semantics(s)
    tree_print(a)

    print("\n"*3)
    te = TypeEngine(a.function_definitions+a.struct_definitions)
    te.run()
