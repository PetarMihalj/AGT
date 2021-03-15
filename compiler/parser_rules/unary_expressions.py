from parser_rules import ParserRule
class UnaryExpression(ParserRule):
    """UnaryExpression : IncrementAfter
                       | IncrementBefore
                       | DecrementAfter
                       | DecrementBefore
                       | FunctionCall
                       | VarName
                       | Literal
                       | '(' Expression ')'
    """

    def __init__(self, r):
        self.unaryExprValue = r[0]
    def rpn(self):
        if type(self) != list:
            return [self.unaryExprValue.rpn()]
        else:
            return self.unaryExprValue.rpn()


class IncrementAfter(ParserRule):
    """IncrementAfter : VarName Inc"""

    def __init__(self, r):
        self.name = r[0]
    def rpn(self):
        return [self.name, "++"]


class IncrementBefore(ParserRule):
    """IncrementBefore : Inc VarName"""

    def __init__(self, r):
        self.name = r[0]
    def rpn(self):
        return ["++", self.name]


class DecrementAfter(ParserRule):
    """DecrementAfter : VarName Dec"""

    def __init__(self, r):
        self.name = r[0]
    def rpn(self):
        return [self.name, "--"]
 


class DecrementBefore(ParserRule):
    """DecrementBefore : Dec VarName"""

    def __init__(self, r):
        self.name = r[0]
    def rpn(self):
        return ["--", self.name]


class FunctionCall(ParserRule):
    """FunctionCall : VarName '(' ArgumentListR ')'"""

    def __init__(self, r):
        self.name = r[0]
        self.argumentListR = r[2]

    def rpn(self):
        return [self]
