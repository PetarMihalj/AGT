import struct_meta_templates
from lexer import Lexer
from parser import Parser
from helpers import tree_print
from typing import List, Tuple
from copy import deepcopy
import parser_rules as pr
from dataclasses import dataclass
import re



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
