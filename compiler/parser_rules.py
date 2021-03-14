import ply.yacc as yacc
import token_rules
from types import MethodType
from helpers import tree_print

import statements
import literals
import binary_expressions
import unary_expressions
import structural


rl = []
rl.extend(statements.rl)
rl.extend(literals.rl)
rl.extend(binary_expressions.rl)
rl.extend(unary_expressions.rl)
rl.extend(structural.rl)


class Parser:
    def __init__(self, lexer, rules_list, **kwargs):
        for cls in rules_list:
            self.injectRule(cls)
            print(f"Injected {cls}")

        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data, **kvargs):
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

    start = 'CompilationUnit'


if __name__ == '__main__':
    data = '''
    void a(u32 p, u32 t){
        //for (a;432;a){a++;}
        while (a){
            a--;
        }
    }
    '''
    lexer = token_rules.Lexer()
    lexer.test(data)
    parser = Parser(lexer, rl, debug=True)
    a = parser.parse(data)
    tree_print(a)
