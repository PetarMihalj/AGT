class Lexer():
    states = (
        ('mlc', 'exclusive'), ('strchar', 'exclusive'),
    )
    #...
    tokens = (
        'INTL', 'BOOLL', 'ID',
        'IF', 'ELSE', 'BREAK', 'FOR', 'WHILE', 'RETURN',
        #...
    )
    t_ADD = r'\+'
    t_SUB = r'-'
    t_MUL = r'\*'
    #...
    reserved = {
        'type': 'TYPE',
        'fn': 'FN',
        'let': 'LET',
        #...
    }
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_INTL(self, t):
        r'(\d+)(|i8|i16|i32|i64)'
        return t
    #...
