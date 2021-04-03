import ply.lex as lex


class Lexer():
    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    states = (
        ('mlc', 'exclusive'),
    )

    tokens = (
        'INTL', 'BOOLL',
        'ID',
        'IF', 'ELSE', 'BREAK', 'FOR', 'WHILE', 'RETURN',
        'GEQ', 'LEQ', 'LT', 'GT', 'EQ', 'NE',
        'STRUCT',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
        'DOT', 'COMMA', 'SEMICOLON', 'ASSIGNMENT', 'AMPERSAND',
        'LET', 'FN'
    )

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MOD = r'%'
    t_AMPERSAND = r'&'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_DOT = r'\.'
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_ASSIGNMENT = r'='
    t_GEQ = r'>='
    t_LEQ = r'<='
    t_GT = r'>'
    t_LT = r'<'
    t_EQ = r'=='
    t_NE = r'!='

    t_FN = r'fn'+' '*20
    t_LET = r'let'+' '*20
    t_IF = r'if'+' '*20
    t_ELSE = r'else'+' '*20
    t_BREAK = r'break'+' '*20
    t_FOR = r'for'+' '*20
    t_WHILE = r'while'+' '*20
    t_RETURN = r'return'+' '*20
    t_STRUCT = r'struct'+' '*20
    t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'

    def t_INTL(self, t):
        r'(-{0,1}\d+)([UuIi]{0,1})(8|16|32|64|128){0,1}'
        return t

    def t_BOOLL(self, t):
        r'true|false|True|False'
        return t

    # MAIN STATE

    def t_COMMENT(self, t):
        r'//.*'
        t.value = t.value[2:]
        pass

    def t_ENTERMLC(self, t):
        r'/\*'
        self.mlc_line = 0
        t.lexer.push_state('mlc')
        pass

    def t_NEWLINE(self, t):
        r'\n'
        self.lexer.lineno += 1
        pass

    def t_SPACE(self, t):
        r'\s'
        pass

    # MULTILINE COMMENT STATE

    def t_mlc_COMMENT(self, t):
        r'\*/'
        self.lexer.lineno += self.mlc_line
        del self.mlc_line
        t.lexer.pop_state()
        pass

    def t_mlc_newline(self, t):
        r'\n'
        self.lexer.lineno += 1
        pass

    def t_mlc_anything(self, t):
        r'.'
        t.value = t.value[2:]
        pass

    # UTILS

    def t_error(self, t):
        print(f"illegal token (main state) at line\
                {t.lexer.lineno}: '{t.value}'")
        self.lexer.skip(1)

    def t_mlc_error(self, t):
        print(f"illegal token (mlc state) at line\
              {t.lexer.lineno}: '{t.value}'")
        self.lexer.skip(1)

    def input(self, data):
        """
        Feed the lexer with data.
        """
        self.lexer.input(data)

    def token(self):
        """
        Get the next token, from data (generator).
        """
        return self.lexer.token()

    def test(self, data):
        """
        Prints out all the tokens
        """
        self.lexer.input(data)
        for tok in self.lexer:
            print(tok)


if __name__ == '__main__':
    data = open('prog1.st').read()
    lexer = Lexer(debug=1)
    lexer.test(data)
