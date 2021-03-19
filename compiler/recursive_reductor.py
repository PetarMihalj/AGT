import parser
import lexer
from types import SimpleNamespace

if __name__ == '__main__':
    data = '''
    struct petar(i32 a, i32 b)

    void a(u32 p, u32 t){
        i32 a;
        a = (a+a)*a;
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
