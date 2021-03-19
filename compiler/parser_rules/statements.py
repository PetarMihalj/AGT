from parser_rules import ParserRule
class Statement(ParserRule):
    '''Statement : AssignmentStatement
                 | DeclarationAssignmentStatement
                 | Expression ';'
                 | DeclarationStatement
                 | IfElseStatement
                 | ForStatement
                 | WhileStatement
                 | BreakStatement
                 | ReturnStatement
                 | BlankStatement
    '''

    def __init__(self, r):
        self.statement = r[0]
    def rpn(self):
        return self.statement.rpn()



class StatementListR(ParserRule):
    """StatementListR : Statement StatementListR
                      | empty
    """

    def __init__(self, r):
        if len(r) == 1:
            self.statement = None
            self.nxt = None
        else:
            self.statement = r[0]
            self.nxt = r[1]

    def rpn(self):
        if self.statement == None:
            return []
        else:
            return [self.statement.rpn()] + self.nxt.rpn()

class BlankStatement(ParserRule):
    "BlankStatement : ';'"
    def __init__(self, r):
        pass

class DeclarationAssignmentStatement(ParserRule):
    """DeclarationAssignmentStatement : Id Id '=' Expression ';'"""

    def __init__(self, r):
        self.typeName = r[0]
        self.name = r[1]
        self.expr = r[3]


class DeclarationStatement(ParserRule):
    """DeclarationStatement : Id Id ';'"""

    def __init__(self, r):
        self.typeName = r[0]
        self.name = r[1]


class AssignmentStatement(ParserRule):
    """AssignmentStatement : Id '=' Expression ';'
                           | Id '=' Expression
    """

    def __init__(self, r):
        self.name = r[0]
        self.expr = r[2]


class IfElseStatement(ParserRule):
    """IfElseStatement : IF '(' Expression ')' Block ELSE Block
    """

    def __init__(self, r):
        self.expr = r[2]
        self.blockIf = r[4]
        self.blockElse = r[6]


class ForStatement(ParserRule):
    """ForStatement : FOR '(' Statement Expression ';' Statement ')' Block
    """

    def __init__(self, r):
        self.statementInit = r[2]
        self.exprCheck = r[3]
        self.statementChange = r[5]
        self.block = r[7]


class WhileStatement(ParserRule):
    """WhileStatement : WHILE '(' Expression ')' Block
    """

    def __init__(self, r):
        self.expr = r[2]
        self.block = r[4]


class ReturnStatement(ParserRule):
    """ReturnStatement : RETURN Expression ';'
                       | RETURN ';'
    """

    def __init__(self, r):
        if len(r) == 3:
            self.expr = r[1]
        else:
            self.expr = None


class BreakStatement(ParserRule):
    """BreakStatement : BREAK INTL ';'
                      | BREAK ';'
    """

    def __init__(self, r):
        if len(r) == 3:
            self.count = r[1]
        else:
            self.count = 1
