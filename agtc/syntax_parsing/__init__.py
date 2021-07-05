def get_syntax_ast(data):
    from ..lexing.lexer import Lexer
    from .syntax_ast import SyntaxParser
    l = Lexer()
    p = SyntaxParser(l)
    parsed = p.parse_syntax(data)
    if p.err_cnt > 0:
        raise RuntimeError("Syntax parsing failed with errors")
    else:
        return parsed
