from parser_rules import ParserRule

class UnaryExpression(ParserRule):
    """UnaryExpression : FunctionCall
                       | Id
                       | Literal
                       | '(' Expression ')'
    """

    def __init__(self, r):
        if r[0]=='(':
            self.unaryExprValue = r[1]
        else:
            self.unaryExprValue = r[0]
    def rpn(self):
        ret = self.unaryExprValue.rpn()
        if type(ret) != list:
            ret = [ret]
        return ret

class FunctionCall(ParserRule):
    """FunctionCall : Id '(' ArgumentListR ')'"""

    def __init__(self, r):
        self.name = r[0]
        self.argumentListR = r[2]

    def rpn(self):
        return [self]

class ArgumentListR(ParserRule):
    """ArgumentListR : Argument ',' ArgumentListR
                     | Argument
                     | empty
    """

    def __init__(self, r):
        if r[0] == 'empty':
            self.argument = None
            self.nxt = None
        elif len(r) == 1:
            self.argument = r[0]
            self.nxt = None
        else:
            self.argument = r[0]
            self.nxt = r[2]

    def rpn(self):
        if self.argument == None:
            return []
        elif self.argument == None:
            return [self.argument.rpn()]
        else:
            return [self.argument.rpn()] + self.nxt.rpn()

class Argument(ParserRule):
    """Argument : Expression"""

    def __init__(self, r):
        self.expr = r[0]

# Priorities are listed from:
# https://en.cppreference.com/w/c/language/operator_precedence

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
