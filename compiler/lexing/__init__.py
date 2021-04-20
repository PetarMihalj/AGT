def get_tokens(data):
    from .lexer import Lexer
    l = Lexer()
    l.input(data)
    return [a for a in l.lexer]

