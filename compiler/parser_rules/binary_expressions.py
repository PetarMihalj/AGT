# Priorities are listed from:
# https://en.cppreference.com/w/c/language/operator_precedence
from parser_rules import ParserRule

class BinaryExpressionPrio3(ParserRule):
    """BinaryExpressionPrio3 : UnaryExpression Mul BinaryExpressionPrio3
                             | UnaryExpression Div BinaryExpressionPrio3
                             | UnaryExpression Mod BinaryExpressionPrio3
                             | UnaryExpression
    """

    def __init__(self, r):
        if len(r) == 1:
            self.left = r[0]
            self.op = None
            self.right = None
        else:
            self.left = r[0]
            self.op = r[1]
            self.right = r[2]

    def rpn(self):
        if self.op == None:
            return self.left.rpn()
        else:
            return self.left.rpn()+self.right.rpn()+[self.op]


class BinaryExpressionPrio4(ParserRule):
    """BinaryExpressionPrio4 : BinaryExpressionPrio3 Add BinaryExpressionPrio4
                             | BinaryExpressionPrio3 Sub BinaryExpressionPrio4
                             | BinaryExpressionPrio3
    """

    def __init__(self, r):
        if len(r) == 1:
            self.left = r[0]
            self.op = None
            self.right = None
        else:
            self.left = r[0]
            self.op = r[1]
            self.right = r[2]

    def rpn(self):
        if self.op == None:
            return self.left.rpn()
        else:
            return self.left.rpn()+self.right.rpn()+[self.op]



class BinaryExpressionPrio6(ParserRule):
    """BinaryExpressionPrio6 : BinaryExpressionPrio4 LessEqual BinaryExpressionPrio6
                             | BinaryExpressionPrio4 GreaterEqual BinaryExpressionPrio6
                             | BinaryExpressionPrio4 Less BinaryExpressionPrio6
                             | BinaryExpressionPrio4 Greater BinaryExpressionPrio6
                             | BinaryExpressionPrio4
    """

    def __init__(self, r):
        if len(r) == 1:
            self.left = r[0]
            self.op = None
            self.right = None
        else:
            self.left = r[0]
            self.op = r[1]
            self.right = r[2]

    def rpn(self):
        if self.op == None:
            return self.left.rpn()
        else:
            return self.left.rpn()+self.right.rpn()+[self.op]


class BinaryExpressionPrio7(ParserRule):
    """BinaryExpressionPrio7 : BinaryExpressionPrio6 NotEqual BinaryExpressionPrio7
                             | BinaryExpressionPrio6 Equal BinaryExpressionPrio7
                             | BinaryExpressionPrio6
    """

    def __init__(self, r):
        if len(r) == 1:
            self.left = r[0]
            self.op = None
            self.right = None
        else:
            self.left = r[0]
            self.op = r[1]
            self.right = r[2]

    def rpn(self):
        if self.op == None:
            return self.left.rpn()
        else:
            return self.left.rpn()+self.right.rpn()+[self.op]


class Expression(ParserRule):
    """Expression : BinaryExpressionPrio7"""

    def __init__(self, r):
        self.expr = r[0]

    def rpn(self):
        return self.expr.rpn()
