from helpers import add
rl = []


@add(rl)
class Statement:
    '''Statement : AssignmentStatement
                 | DeclarationAssignmentStatement
                 | Expression ';'
                 | DeclarationStatement
                 | IfElseStatement
                 | ForStatement
                 | WhileStatement
                 | BreakStatement
                 | ReturnStatement
    '''

    def __init__(self, r):
        self.value = r[0]


@add(rl)
class StatementListR:
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


@add(rl)
class DeclarationAssignmentStatement:
    """DeclarationAssignmentStatement : TypeName ID '=' Expression ';'"""

    def __init__(self, r):
        self.typeName = r[0]
        self.name = r[1]
        self.expr = r[3]


@add(rl)
class DeclarationStatement:
    """DeclarationStatement : TypeName ID ';'"""

    def __init__(self, r):
        self.typeName = r[0]
        self.name = r[1]


@add(rl)
class AssignmentStatement:
    """AssignmentStatement : ID '=' Expression ';'"""

    def __init__(self, r):
        self.name = r[0]
        self.expr = r[2]


@add(rl)
class IfElseStatement:
    """IfElseStatement : IF '(' Expression ')' Block ELSE Block
    """

    def __init__(self, r):
        self.expr = r[2]
        self.blockIf = r[4]
        self.blockElse = r[6]


@add(rl)
class ForStatement:
    """ForStatement : FOR '(' Statement ';' Expression ';' Statement ')' Block
    """

    def __init__(self, r):
        self.statementInit = r[2]
        self.exprCheck = r[4]
        self.statementChange = r[6]
        self.block = r[8]


@add(rl)
class WhileStatement:
    """WhileStatement : WHILE '(' Expression ')' Block
    """

    def __init__(self, r):
        self.expr = r[2]
        self.block = r[4]


@add(rl)
class ReturnStatement:
    """ReturnStatement : RETURN Expression ';'
                       | RETURN ';'
    """

    def __init__(self, r):
        if len(r) == 3:
            self.expr = r[1]
        else:
            self.expr = None


@add(rl)
class BreakStatement:
    """BreakStatement : BREAK INTL ';'
                      | BREAK ';'
    """

    def __init__(self, r):
        if len(r) == 3:
            self.count = r[1]
        else:
            self.count = 1
