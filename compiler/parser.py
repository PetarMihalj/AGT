import inspect
import parser_rules
import ply.yacc as yacc
from types import MethodType

class Parser:
    def __init__(self, lexer, **kwargs):
        for mod in parser_rules.modules:
            for name, obj in inspect.getmembers(mod):
                if inspect.isclass(obj):
                    self.injectRule(obj)
                    print(f"Injected {obj}")

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
    import lexer
    from helpers import tree_print
    lexer = lexer.Lexer()
    lexer.test(data)
    parser = Parser(lexer, debug=True)
    a = parser.parse(data)
    tree_print(a)
