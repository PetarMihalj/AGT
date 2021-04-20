class Lexer():

    def __init__(self, **kwargs):
        import ply.lex as lex
        self.lexer = lex.lex(object=self, **kwargs)

    states = (
        ('mlc', 'exclusive'),
    )

    tokens = (
        'INTL', 'BOOLL',
        'ID',
        'IF', 'ELSE', 'BREAK', 'FOR', 'WHILE', 'RETURN',
        'GE', 'LE', 'LT', 'GT', 'EQ', 'NE',
        'STRUCT',
        'ADD', 'SUB', 'MUL', 'DIV', 'MOD',
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
        'DOT', 'COMMA', 'SEMICOLON', 'ASSIGNMENT',
        'LET', 'FN', 'ARROW', 'TYPE',
        'LANGLE', 'RANGLE', 'DEREF', 'ADDRESS'
    )

    t_ADD = r'\+'
    t_SUB = r'-'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_MOD = r'%'
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
    t_GE = r'>='
    t_LE = r'<='
    t_LANGLE = r'<'
    t_RANGLE = r'>'
    t_GT = r'>!'
    t_LT = r'<!'
    t_EQ = r'=='
    t_NE = r'!='
    t_DEREF = r'!'
    t_ADDRESS = r'@'
    t_ARROW = r'->'

    reserved = {
        'type': 'TYPE',
        'fn': 'FN',
        'let': 'LET',
        'if': 'IF',
        'else': 'ELSE',
        'break': 'BREAK',
        'for': 'FOR',
        'while': 'WHILE',
        'return': 'RETURN',
        'struct': 'STRUCT',
    }

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_INTL(self, t):
        r'(\d+)([Ii]{0,1})(\d+){0,1}'
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


    def token(self):
        """
        Get the next token, from data (generator).
        """
        res = self.lexer.token()
        self.lexpos = self.lexer.lexpos
        self.lineno = self.lexer.lineno
        return res

    def input(self, data):
        self.lexer.input(data)
