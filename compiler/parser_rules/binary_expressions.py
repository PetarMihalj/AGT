from helpers import add
rl = []


# Priorities are listed from:
# https://en.cppreference.com/w/c/language/operator_precedence

@add(rl)
class BinaryExpressionPrio3:
    """BinaryExpressionPrio3 : UnaryExpression '*' BinaryExpressionPrio3
                             | UnaryExpression '/' BinaryExpressionPrio3
                             | UnaryExpression '%' BinaryExpressionPrio3
                             | UnaryExpression
    """

    def __init__(self, r):
        if len(r) == 1:
            self.left = r[0]
        else:
            self.left = r[0]
            self.op = r[1]
            self.right = r[2]


@add(rl)
class BinaryExpressionPrio4:
    """BinaryExpressionPrio4 : BinaryExpressionPrio3 '+' BinaryExpressionPrio4
                             | BinaryExpressionPrio3 '-' BinaryExpressionPrio4
                             | BinaryExpressionPrio3
    """

    def __init__(self, r):
        if len(r) == 1:
            self.left = r[0]
        else:
            self.left = r[0]
            self.op = r[1]
            self.right = r[2]


@add(rl)
class BinaryExpressionPrio6:
    """BinaryExpressionPrio6 : BinaryExpressionPrio4 LEQ BinaryExpressionPrio6
                             | BinaryExpressionPrio4 GEQ BinaryExpressionPrio6
                             | BinaryExpressionPrio4 LT BinaryExpressionPrio6
                             | BinaryExpressionPrio4 GT BinaryExpressionPrio6
                             | BinaryExpressionPrio4
    """

    def __init__(self, r):
        if len(r) == 1:
            self.left = r[0]
        else:
            self.left = r[0]
            self.op = r[1]
            self.right = r[2]


@add(rl)
class BinaryExpressionPrio7:
    """BinaryExpressionPrio7 : BinaryExpressionPrio6 NEQ BinaryExpressionPrio7
                             | BinaryExpressionPrio6 EQ BinaryExpressionPrio7
                             | BinaryExpressionPrio6
    """

    def __init__(self, r):
        if len(r) == 1:
            self.left = r[0]
        else:
            self.left = r[0]
            self.op = r[1]
            self.right = r[2]


@add(rl)
class Expression:
    """Expression : BinaryExpressionPrio7"""

    def __init__(self, r):
        self.expr = r[0]
