class ParserRule:
    pass


class CompilationUnit(ParserRule):
    '''CompilationUnit : DefinitionList'''

    def __init__(self, r):
        self.definitionList = r[0]


class DefinitionList(ParserRule):
    """DefinitionList : FunctionDefinition DefinitionList
                       | StructDefinition DefinitionList
                       | empty
    """

    def __init__(self, r):
        if len(r) == 1:
            self.flist = []
            self.slist = []
        else:
            if isinstance(r[0], FunctionDefinition):
                self.flist = [r[0]] + r[1].flist
                self.slist = [] + r[1].slist
            elif isinstance(r[0], StructDefinition):
                self.flist = [] + r[1].flist
                self.slist = [r[0]] + r[1].slist


class StructDefinition(ParserRule):
    """StructDefinition : STRUCT Expression Block
    """

    def __init__(self, r):
        print(r)
        self.expr = r[1]
        self.block = r[2]


class FunctionDefinition(ParserRule):
    """FunctionDefinition : FN Expression Block
                          | FN Expression ARROW Expression Block
    """

    def __init__(self, r):
        if len(r) == 3:
            self.expr = r[1]
            self.block = r[2]
            self.expr_ret = None
        elif len(r) == 5:
            self.expr = r[1]
            self.expr_ret = r[3]
            self.block = r[4]


class Block(ParserRule):
    "Block : LBRACE StatementList RBRACE"

    def __init__(self, r):
        self.statementList = r[1].list


##
# STATEMENTS
##

class StatementList(ParserRule):
    """StatementList : Statement StatementList
                     | Statement
    """

    def __init__(self, r):
        if len(r) == 1:
            self.list = [r[0]]
        else:
            self.list = [r[0]]+r[1].list


class Statement(ParserRule):
    '''Statement : AssignmentStatement
                 | InitStatement
                 | ExpressionStatement
                 | IfElseStatement
                 | ForStatement
                 | WhileStatement
                 | BreakStatement
                 | ReturnStatement
                 | BlockStatement
                 | BlankStatement
                 | TypeStatement
                 | DeclarationStatement
    '''

    def __init__(self, r):
        self.statement = r[0]


class ExpressionStatement(ParserRule):
    """ExpressionStatement : Expression SEMICOLON"""

    def __init__(self, r):
        self.expr = r[0]


class DeclarationStatement(ParserRule):
    """DeclarationStatement : Expression Expression SEMICOLON"""

    def __init__(self, r):
        self.expr1 = r[0]
        self.expr2 = r[1]


class TypeStatement(ParserRule):
    """TypeStatement : TYPE Expression ASSIGNMENT Expression SEMICOLON"""

    def __init__(self, r):
        self.left = r[1]
        self.right = r[3]


class BlankStatement(ParserRule):
    "BlankStatement : SEMICOLON"

    def __init__(self, r):
        pass


class BlockStatement(ParserRule):
    "BlockStatement : Block"

    def __init__(self, r):
        self.block = r[0]


class InitStatement(ParserRule):
    """InitStatement : LET Expression ASSIGNMENT Expression SEMICOLON
    """

    def __init__(self, r):
        self.name = r[1]
        self.expr = r[3]


class AssignmentStatement(ParserRule):
    """AssignmentStatement : Expression ASSIGNMENT Expression SEMICOLON
    """

    def __init__(self, r):
        self.left = r[0]
        self.right = r[2]


class IfElseStatement(ParserRule):
    """IfElseStatement : IF LPAREN Expression RPAREN Block ELSE Block
                       | IF LPAREN Expression RPAREN Block
    """

    def __init__(self, r):
        if len(r) == 7:
            self.expr = r[2]
            self.blockIf = r[4]
            self.blockElse = r[6]
        else:
            self.expr = r[2]
            self.blockIf = r[4]
            self.blockElse = None


class ForStatement(ParserRule):
    """ForStatement : FOR LPAREN Statement Expression\
            SEMICOLON Statement RPAREN Block
    """

    def __init__(self, r):
        self.statementInit = r[2]
        self.exprCheck = r[3]
        self.statementChange = r[5]
        self.block = r[7]


class WhileStatement(ParserRule):
    """WhileStatement : WHILE LPAREN Expression RPAREN Block
    """

    def __init__(self, r):
        self.exprCheck = r[2]
        self.block = r[4]


class ReturnStatement(ParserRule):
    """ReturnStatement : RETURN Expression SEMICOLON
                       | RETURN SEMICOLON
    """

    def __init__(self, r):
        if len(r) == 3:
            self.expr = r[1]
        else:
            self.expr = None


class BreakStatement(ParserRule):
    """BreakStatement : BREAK IntLiteral SEMICOLON
                      | BREAK SEMICOLON
    """

    def __init__(self, r):
        if len(r) == 3:
            self.count = r[1].value
        else:
            self.count = 1


##
# EXPRESSIONS
##

class ExpressionList(ParserRule):
    """ExpressionList : Expression COMMA ExpressionList
                      | Expression
                      | empty
    """

    def __init__(self, r):
        if r[0] is None:
            self.list = []
        elif len(r) == 1:
            self.list = [r[0]]
        else:
            self.list = [r[0]] + r[2].list


# Priorities are listed from:
# https://en.cppreference.com/w/c/language/operator_precedence
precedence = (
    ('left', 'COMMA'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV', 'MOD'),
    ('left', 'LE', 'GE', 'LT', 'GT', 'EQ', 'NE'),
    ('left', 'DOT', 'DEREF'),
    ('right', 'ADDRESS'),
    ('left', 'LPAREN', 'LBRACE'),
    ('left', 'LANGLE', 'RANGLE'),
)


class Expression(ParserRule):
    """Expression : BinaryExpression
                  | UnaryExpression
                  | IdExpression
    """

    def __init__(self, r):
        self.expr = r[0]


class IdExpression(ParserRule):
    """IdExpression : ID"""

    def __init__(self, r):
        self.id = r[0]


class BinaryExpression(ParserRule):
    """BinaryExpression : Expression ADD Expression
                        | Expression SUB Expression
                        | Expression MUL Expression
                        | Expression DIV Expression
                        | Expression MOD Expression
                        | Expression LE Expression
                        | Expression GE Expression
                        | Expression LT Expression
                        | Expression GT Expression
                        | Expression EQ Expression
                        | Expression NE Expression
    """

    def __init__(self, r):
        self.left = r[0]
        self.op = r[1]
        self.right = r[2]


class UnaryExpression(ParserRule):
    """UnaryExpression : LiteralExpression
                       | ParenthesesCallExpression
                       | BracketCallExpression
                       | DotExpression
                       | ParenthesesExpression
                       | DereferenceExpression
                       | AddressExpression
                       | AngleCallExpression
    """

    def __init__(self, r):
        self.expr = r[0]


class ParenthesesExpression(ParserRule):
    """ParenthesesExpression : LPAREN Expression RPAREN"""

    def __init__(self, r):
        self.expr = r[1]


class AngleCallExpression(ParserRule):
    """AngleCallExpression : Expression LANGLE ExpressionList RANGLE"""

    def __init__(self, r):
        self.expr = r[0]
        self.expr_list = r[2].list


class ParenthesesCallExpression(ParserRule):
    """ParenthesesCallExpression : Expression LPAREN\
            ExpressionList RPAREN"""

    def __init__(self, r):
        self.expr = r[0]
        self.expr_list = r[2].list


class DotExpression(ParserRule):
    """DotExpression : Expression DOT Expression
    """

    def __init__(self, r):
        self.left = r[0]
        self.right = r[2]


class BracketCallExpression(ParserRule):
    """BracketCallExpression : Expression LBRACKET Expression\
            RBRACKET"""

    def __init__(self, r):
        self.expr1 = r[0]
        self.expr2 = r[2]


class DereferenceExpression(ParserRule):
    """DereferenceExpression : Expression DEREF"""

    def __init__(self, r):
        self.expr = r[0]


class AddressExpression(ParserRule):
    """AddressExpression : ADDRESS Expression"""

    def __init__(self, r):
        self.expr = r[1]


class LiteralExpression(ParserRule):
    '''LiteralExpression : IntLiteral
                         | BoolLiteral
    '''

    def __init__(self, r):
        self.value = r[0]


class IntLiteral(ParserRule):
    '''IntLiteral : INTL'''

    def __init__(self, r):
        self.size = 32
        if 'i' in r[0]:
            sp = r[0].split('i')
            self.value = int(sp[0])
            if len(sp) == 2:
                self.size = int(sp[1])
            else:
                self.size = 32
        elif 'I' in r[0]:
            sp = r[0].split('I')
            self.value = -1 * int(sp[0])
            if len(sp) == 2:
                self.size = int(sp[1])
            else:
                self.size = 32
        else:
            self.value = int(r[0])
            self.size = 32


class BoolLiteral(ParserRule):
    '''BoolLiteral : BOOLL'''

    def __init__(self, r):
        self.value = r[0] in ('True', 'true')
