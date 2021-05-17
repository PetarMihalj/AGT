import ply.lex as lex

char_code = {
    "\\n" : 10,
    "\\t" : 9,
    "\\0" : 0,
    "\\\"" : 34,
    "\\\'" : 39,
}

SINGLEQUOTE = "'"
DOUBLEQUOTE = '"'
BACKSLASH = "\\"

for i in range(32, 126+1):
    if i not in [34, 39]:
        char_code[chr(i)] = i 

class Lexer():
    def __init__(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)

    states = (
        ('mlc', 'exclusive'),
        ('strchar', 'exclusive'),
    )

    tokens = (
        'INTL', 
        'ID',
        'TRUE', 'FALSE',
        'IF', 'ELSE', 'BREAK', 'FOR', 'WHILE', 'RETURN',
        'GE', 'LE', 'LT', 'GT', 'EQ', 'NE',
        'STRUCT',
        'ADD', 'SUB', 'MUL', 'DIV', 'MOD',
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
        'DOT', 'COMMA', 'SEMICOLON', 'ASSIGNMENT',
        'LET', 'FN', 'ARROW', 'TYPE',
        'LANGLE', 'RANGLE', 'DEREF', 'ADDRESS',
        'STRINGL', 'CHARL',
        'AND', 'OR',
        'NOT'
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
    t_AND = r'&'
    t_OR = r'\|'
    t_NOT = r'~'

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
        'true': 'TRUE',
        'True': 'TRUE',
        'false': 'FALSE',
        'False': 'FALSE',
    }

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_INTL(self, t):
        r'(\d+)(i8|i16|i32|i64|)'
        return t

    # STRING STATE

    def t_ENTER_STRCHAR(self, t):
        r'''['"]'''

        t.lexer.push_state('strchar')
        self.ending_quote = t.value
        self.escape_on = False
        self.chars = []


    def t_strchar_EXIT_MAYBE(self, t):
        r'''['"]'''

        if self.escape_on:
            self.chars.append(char_code[f'{BACKSLASH}{t.value}'])
            self.escape_on = False
        else:
            if t.value == self.ending_quote:
                if t.value == SINGLEQUOTE:
                    if len(self.chars) != 1:
                        raise RuntimeError("Character must be singular")
                    t.type = self.reserved.get(t.value, 'CHARL')
                    t.value = self.chars[0]
                else:
                    self.chars.append(char_code[f'{BACKSLASH}0'])
                    t.type = self.reserved.get(t.value, 'STRINGL')
                    t.value = self.chars
                t.lexer.pop_state()
                del self.chars
                del self.escape_on
                del self.ending_quote
                return t
            else:
                self.chars.append(char_code[f'{BACKSLASH}{t.value}'])


    def t_strchar_ESCAPE(self, t):
        r'\\'
        if self.escape_on:
            self.chars.append(char_code['\\'])
            self.escape_on = False
        else:
            self.escape_on = True

    def t_strchar_OTHERS(self, t):
        r'.'
        if self.escape_on:
            v = f'\\{t.value}'
            if v not in char_code:
                raise RuntimeError("Bad escape!")
            else:
                self.chars.append(char_code[v])
            self.escape_on = False
        else:
            v = f'{t.value}'
            if v not in char_code:
                raise RuntimeError("Bad character!")
            else:
                self.chars.append(char_code[v])

    def t_strchar_WS(self, t):
        r'[\s]'
        pass

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

    def t_strchar_error(self, t):
        print(f"illegal token (strchar state) at line\
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
