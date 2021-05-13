import sys
import inspect
from . import parser_rules
import ply.yacc as yacc
from types import MethodType


class SyntaxParser:
    def __init__(self, lexer, **kwargs):
        for name, obj in inspect.getmembers(parser_rules):
            if inspect.isclass(obj)\
                    and issubclass(obj, parser_rules.ParserRule)\
                    and obj is not parser_rules.ParserRule:
                self.injectRule(obj)
                # print(f"Injected {obj}")
        self.precedence = parser_rules.precedence

        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self, write_tables=False, **kwargs)

    def parse_syntax(self, data, **kvargs):
        return self.parser.parse(data, lexer=self.lexer,
                tracking = True, **kvargs)

    def injectRule(self, rule_class):
        def method(self, p):
            obj = rule_class(p[1:])
            p[0] = obj
            obj.lexspan = p.lexspan(0)
            obj.linespan = p.linespan(0)
        bound = MethodType(method, self)
        bound.__func__.__doc__ = rule_class.__doc__
        self.__setattr__(f"p_{rule_class}", bound)

    def p_empty(self, p):
        '''empty :'''
        pass

    def p_error(self, p):
        print(f"ERROR: {p}")

    start = 'CompilationUnit'





