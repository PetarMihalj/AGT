
from parser_rules import ParserRule
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


class Literal(ParserRule):
    '''Literal : IntLiteral
               | BoolLiteral
               | CharLiteral
    '''

    def __init__(self, r):
        self.value = r[0]
