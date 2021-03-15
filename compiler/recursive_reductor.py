import parser
import lexer
from types import SimpleNamespace

if __name__ == '__main__':
    data = '''
    void a(u32 p, u32 t){
        for (a=2;a<3;a=a+3){a++;}
        while (a){
            a=a-a;
        };
    }
    '''
    print(data)
    from helpers import tree_print
    lexer = lexer.Lexer()
    parser = parser.Parser(lexer, debug=True)
    a = parser.parse(data)
    tree_print(a)
    t = a.rpn()
    tree_print(t)
