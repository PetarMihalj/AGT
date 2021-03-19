from parser_rules import ParserRule

class Id(ParserRule):
    "Id : ID"
    def __init__(self, r):
        self.name = r[0]

class Add(ParserRule):
    "Add : '+'"
class Sub(ParserRule):
    "Sub : '-'"
class Mul(ParserRule):
    "Mul : '*'"
class Div(ParserRule):
    "Div : '/'"
class Mod(ParserRule):
    "Mod : '%'"

class Equal(ParserRule):
    '''Equal : EQ'''
class NotEqual(ParserRule):
    '''NotEqual : NE'''
class LessEqual(ParserRule):
    '''LessEqual : GEQ'''
class GreaterEqual(ParserRule):
    '''GreaterEqual : LEQ'''
class Less(ParserRule):
    '''Less : LT'''
class Greater(ParserRule):
    '''Greater : GT'''

# Literals

class Literal(ParserRule):
    '''Literal : IntLiteral
               | BoolLiteral
               | CharLiteral
    '''

    def __init__(self, r):
        self.value = r[0]

class IntLiteral(ParserRule):
    '''IntLiteral : INTL'''

    def __init__(self, r):
        self.signed = True
        self.size = 32
        if 'u' in r[0]:
            self.signed = False
            sp = r[0].split('u')
            self.value = int(sp[0])
            if len(sp[1]) > 0:
                self.size = int(sp[1])
        elif 'i' in r[0]:
            sp = r[0].split('i')
            self.value = int(sp[0])
            if len(sp[1]) > 0:
                self.size = int(sp[1])
        else:
            self.value = int(r[0])


class CharLiteral(ParserRule):
    '''CharLiteral : CHARL'''

    def __init__(self, r):
        self.value = ord(r[0][1])


class BoolLiteral(ParserRule):
    '''BoolLiteral : BOOLL'''

    def __init__(self, r):
        self.value = r[0] in ('True', 'true')
