def get_syntax_ast(data):
    from ..lexing.lexer import Lexer
    from .syntax_ast import SyntaxParser
    l = Lexer()
    p = SyntaxParser(l, debug=False)
    return p.parse_syntax(data)
