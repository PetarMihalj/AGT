import sys
import inspect
import parser_rules
import ply.yacc as yacc
from lexer import Lexer
from types import MethodType
from helpers import tree_print


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
        return self.parser.parse(data, lexer=self.lexer, **kvargs)

    def injectRule(self, rule_class):
        def method(self, p):
            obj = rule_class(p[1:])
            p[0] = obj
        bound = MethodType(method, self)
        bound.__func__.__doc__ = rule_class.__doc__
        self.__setattr__(f"p_{rule_class}", bound)

    def p_empty(self, p):
        '''empty :'''
        pass

    def p_error(self, p):
        print(f"ERROR: {p}")

    start = 'CompilationUnit'


def compile_syntactic_ast(data):
    lexer = Lexer()
    parser = SyntaxParser(lexer, debug=False)
    s = parser.parse_syntax(data)
    return s


if __name__ == '__main__':
    data = open(sys.argv[1]).read()
    syn_ast = compile_syntactic_ast(data)
    tree_print(syn_ast)

