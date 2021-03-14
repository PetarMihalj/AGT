from helpers import add
rl = []


@add(rl)
class UnaryExpression:
    """UnaryExpression : Negate
                       | IncrementAfter
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


@add(rl)
class IncrementAfter:
    """IncrementAfter : VarName INC"""

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class IncrementBefore:
    """IncrementBefore : INC VarName"""

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class DecrementAfter:
    """DecrementAfter : VarName DEC"""

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class DecrementBefore:
    """DecrementBefore : DEC VarName"""

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class Negate:
    """Negate : '-' VarName"""

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class FunctionCall:
    """FunctionCall : VarName '(' ArgumentListR ')'"""

    def __init__(self, r):
        self.name = r[0]
        self.argumentListR = r[2]
