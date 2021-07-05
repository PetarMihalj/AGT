def get_tokens(data):
    from .lexer import Lexer
    l = Lexer()
    l.input(data)
    tokens = [a for a in l.lexer]
    if l.err_cnt > 0:
        raise RuntimeError("Lexer failed with errors")
    else:
        return tokens

