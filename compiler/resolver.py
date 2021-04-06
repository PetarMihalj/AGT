import struct_meta_templates
from lexer import Lexer
from parser import Parser
from helpers import tree_print
from typing import List, Tuple
from copy import deepcopy
import parser_rules as pr
from dataclasses import dataclass
import re


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

# STRUCT META TEMPLATES


class Resolver:
    def __init__(self, tree):
        self.sm = ScopeManager()
        self.smt_check = struct_meta_templates.check_all

        # name -> def
        self.func = dict()
        self.types = dict()

        self.functionTemplates = [
            d for d in tree.definitionList
            if isinstance(d, pr.FunctionDefinition)
        ]
        self.structTemplates = [
            d for d in tree.definitionList
            if isinstance(d, pr.StructDefinition)
        ]
        mainl = [
            d for d in tree.definitionList
            if isinstance(d, pr.FunctionDefinition)
            and d.name == 'main'
            and len(d.parameterList) == 0
            and len(d.typeParameterList) == 0
            and d.returnType == "void"
        ]
        if len(mainl) > 1:
            raise RuntimeError("multiple mains")
        if len(mainl) == 0:
            raise RuntimeError("no mains found")
        self.main = mainl[0]

    def go(self):
        self.main.resolve(self)


if __name__ == '__main__':
    data = open('prog1.st').read()
    lexer = Lexer()
    lexer.test(data)
    parser = Parser(lexer, debug=True)
    a = parser.parse(data)
    tree_print(a)
    tree_print(a)
