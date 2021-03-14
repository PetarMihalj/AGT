from helpers import add
rl = []


@add(rl)
class IntLiteral:
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


@add(rl)
class CharLiteral:
    '''CharLiteral : CHARL'''

    def __init__(self, r):
        self.value = ord(r[0][1])


@add(rl)
class BoolLiteral:
    '''BoolLiteral : BOOLL'''

    def __init__(self, r):
        self.value = r[0] in ('True', 'true')


@add(rl)
class Literal:
    '''Literal : IntLiteral
               | BoolLiteral
               | CharLiteral
    '''

    def __init__(self, r):
        self.value = r[0]
