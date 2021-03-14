import ply.lex as lex


class Lexer():
    tokens = (
        'INC', 'DEC',
        'INTL', 'BOOLL', 'CHARL',
        'ID',
        'IF', 'ELSE', 'BREAK', 'FOR', 'WHILE', 'RETURN',
        'GEQ', 'LEQ', 'LT', 'GT', 'EQ', 'NEQ',
    )

    states = (
        ('mlc', 'exclusive'),
    )

    literals = "+-*/()[]{},;="

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # MAIN STATE

    def t_COMMENT(self, t):
        r'//.*'
        t.value = t.value[2:]
        pass

    def t_ENTERMLC(self, t):
        r'/\*'
        self.mlc = ""
        self.mlc_line = t.lexer.lineno
        t.lexer.push_state('mlc')
        pass

    def t_NEWLINE(self, t):
        r'\n'
        t.lexer.lineno += 1
        pass

    def t_SPACE(self, t):
        r'\s'
        pass

    # ----- FLOW CONTROL

    def t_IF(self, t):
        r'if'
        return t

    def t_ELSE(self, t):
        r'else'
        return t

    def t_BREAK(self, t):
        r'break'
        return t

    def t_FOR(self, t):
        r'for'
        return t

    def t_WHILE(self, t):
        r'while'
        return t

    def t_RETURN(self, t):
        r'return'
        return t

    # ---- BIG OPERATORS
    def t_INC(self, t):
        r'\+\+'
        return t

    def t_DEC(self, t):
        r'\-\-'
        return t

    def t_GEQ(self, t):
        r'>='
        return t

    def t_LEQ(self, t):
        r'<='
        return t

    def t_GT(self, t):
        r'>'
        return t

    def t_LT(self, t):
        r'<'
        return t

    def t_EQ(self, t):
        r'=='
        return t

    def t_NEQ(self, t):
        r'=='
        return t

    # ----- BUILTIN TYPES
    """

    def t_INTTYPE(self, t):
        r'(int|uint|[UuIi])(8|16|32|64|128){0,1}'
        return t

    def t_BOOLTYPE(self, t):
        r'bool|boolean'
        return t

    def t_CHARTYPE(self, t):
        r'char'
        return t

    def t_VOIDTYPE(self, t):
        r'void'
        return t

    def t_VARTYPE(self, t):
        r'var'
        return t
    """

    # ----- CONST LITERALS

    def t_INTL(self, t):
        r'(-{0,1}\d+)([UuIi]{0,1})(8|16|32|64|128){0,1}'
        return t

    def t_BOOLL(self, t):
        r'true|false|True|False'
        return t

    def t_CHARL(self, t):
        r"'[^']'"
        return t

    # ---- ID

    def t_ID(self, t):
        r'[a-zA-z_][a-zA-z_0-9]*'
        return t

    # MULTILINE COMMENT STATE

    def t_mlc_COMMENT(self, t):
        r'\*/'
        t.value = self.mlc
        t.lineno = self.mlc_line
        del self.mlc, self.mlc_line
        t.lexer.pop_state()
        return t

    def t_mlc_newline(self, t):
        r'\n'
        self.mlc += t.value
        t.lexer.lineno += 1
        pass

    def t_mlc_anything(self, t):
        r'.'
        self.mlc += t.value
        t.value = t.value[2:]
        pass

    # UTILS

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()

    def test(self, data):
        self.lexer.input(data)
        for tok in self.lexer:
            print(tok)


if __name__ == '__main__':
    lexer = Lexer(debug=1)
    data = '''
    3u+5
    True
    true
    'a'
    /
    *
    "fasdfas"
    '''
    data = open('ex2.st').read()
    lexer.test(data)
