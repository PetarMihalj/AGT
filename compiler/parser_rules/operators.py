from parser_rules import ParserRule

class Add(ParserRule):
    "Add : '+'"
    def tree_print(self, prefix):
        print(f"{prefix} {type(self).__name__}")

class Sub(ParserRule):
    "Sub : '-'"
class Mul(ParserRule):
    "Mul : '*'"
class Div(ParserRule):
    "Div : '/'"
class Mod(ParserRule):
    "Mod : '%'"
class Inc(ParserRule):
    '''Inc : INC'''
class Dec(ParserRule):
    '''Dec : DEC'''

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
