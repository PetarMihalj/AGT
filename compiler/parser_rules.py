class ParserRule:
    pass

##
# STRUCTURAL
##


class CompilationUnit(ParserRule):
    '''CompilationUnit : DefinitionListR'''

    def __init__(self, r):
        self.definitionList = r[0]


class DefinitionListR(ParserRule):
    """DefinitionListR : FunctionDefinition DefinitionListR
                       | StructDefinition DefinitionListR
                       | empty
    """

    def __init__(self, r):
        if len(r) == 1:
            self.definition = None
            self.nxt = None
        else:
            self.definition = r[0]
            self.nxt = r[1]


class FunctionDefinition(ParserRule):
    """FunctionDefinition : ID ID LPAREN ParameterListR RPAREN Block
                          | ID ID LT TypeParameterListR GT LPAREN ParameterListR RPAREN Block 
    """
    """StructDefinition : STRUCT ID LT TypeParameterListR GT\
            LBRACE StructMemberDeclarationListR RBRACE
            """

    def __init__(self, r):
        if len(r) == 6:
            self.returnType = r[0]
            self.name = r[1]
            self.typeParameterList = []
            self.parameterList = r[3]
            self.block = r[5]
        else:
            self.returnType = r[0]
            self.name = r[1]
            self.typeParameterList = r[3]
            self.parameterList = r[6]
            self.block = r[8]


class ParameterListR(ParserRule):
    """ParameterListR : Parameter COMMA ParameterListR
                     | Parameter
                     | empty
    """

    def __init__(self, r):
        if r[0] == 'empty':
            self.parameter = None
            self.nxt = None
        elif len(r) == 1:
            self.parameter = r[0]
            self.nxt = None
        else:
            self.parameter = r[0]
            self.nxt = r[2]


class Parameter(ParserRule):
    """Parameter : Type ID"""

    def __init__(self, r):
        self.type = r[0]
        self.name = r[1]


class Type(ParserRule):
    """Type : ID PointerListR
            | ID LT TypeParameterListR GT PointerListR
    """

    def __init__(self, r):
        if len(r) == 2:
            self.name = r[0]
            self.typeParameterList = []
            self.ptr_cnt = r[1].sz
        else:
            self.name = r[0]
            self.typeParameterList = r[2]
            self.ptr_cnt = r[4].sz


class PointerListR(ParserRule):
    """PointerListR : TIMES PointerListR
                    | empty
    """

    def __init__(self, r):
        if len(r) == 2:
            self.sz = r[1].sz+1
        else:
            self.sz = 0


class Block(ParserRule):
    "Block : LBRACE StatementListR RBRACE"

    def __init__(self, r):
        self.statementList = r[1]


class StructDefinition(ParserRule):
    """StructDefinition : STRUCT ID LT TypeParameterListR GT\
            LBRACE StructMemberDeclarationListR RBRACE
                        | STRUCT ID\
            LBRACE StructMemberDeclarationListR RBRACE
    """

    def __init__(self, r):
        self.typeName = r[1]
        self.typeParameterList = r[3]
        self.parameterList = r[6]


class TypeParameterListR(ParserRule):
    """TypeParameterListR : TypeParameter COMMA TypeParameterListR
                     | TypeParameter
                     | empty
    """

    def __init__(self, r):
        if r[0] == 'empty':
            self.typeParameter = None
            self.nxt = None
        elif len(r) == 1:
            self.typeParameter = r[0]
            self.nxt = None
        else:
            self.typeParameter = r[0]
            self.nxt = r[2]


class TypeParameter(ParserRule):
    """TypeParameter : ID"""

    def __init__(self, r):
        self.typeName = r[0]


class StructMemberDeclarationListR(ParserRule):
    """StructMemberDeclarationListR : DeclarationStatement\
                                        StructMemberDeclarationListR
                                     | empty
    """

    def __init__(self, r):
        if r[0] == 'empty':
            self.declarationStatement = None
            self.nxt = None
        elif len(r) == 1:
            self.declarationStatement = r[0]
            self.nxt = None
        else:
            self.declarationStatement = r[0]
            self.nxt = r[1]

##
# STATEMENTS
##


class Statement(ParserRule):
    '''Statement : AssignmentStatement
                 | DeclarationAssignmentStatement
                 | DeclarationFunctionCallStatement
                 | DeclarationStatement
                 | Expression SEMICOLON
                 | IfElseStatement
                 | ForStatement
                 | WhileStatement
                 | BreakStatement
                 | ReturnStatement
                 | BlockStatement
                 | BlankStatement
    '''

    def __init__(self, r):
        self.statement = r[0]


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


class BlankStatement(ParserRule):
    "BlankStatement : ';'"

    def __init__(self, r):
        pass


class BlockStatement(ParserRule):
    "BlockStatement : Block"

    def __init__(self, r):
        self.block = r[0]


class DeclarationAssignmentStatement(ParserRule):
    """DeclarationAssignmentStatement : Type ID ASSIGNMENT\
                                        Expression SEMICOLON"""

    def __init__(self, r):
        self.type = r[0]
        self.name = r[1]
        self.expr = r[3]


class DeclarationFunctionCallStatement(ParserRule):
    """DeclarationFunctionCallStatement : Type FunctionCall SEMICOLON"""

    def __init__(self, r):
        self.type = r[0]
        self.funcCall = r[1]


class DeclarationStatement(ParserRule):
    """DeclarationStatement : Type ID SEMICOLON"""

    def __init__(self, r):
        self.type = r[0]
        self.name = r[1]


class AssignmentStatement(ParserRule):
    """AssignmentStatement : IdListR ASSIGNMENT Expression SEMICOLON
                           | IdListR ASSIGNMENT Expression
    """

    def __init__(self, r):
        self.name = r[0]
        self.expr = r[2]


class IfElseStatement(ParserRule):
    """IfElseStatement : IF LPAREN Expression RPAREN Block ELSE Block
    """

    def __init__(self, r):
        self.expr = r[2]
        self.blockIf = r[4]
        self.blockElse = r[6]


class ForStatement(ParserRule):
    """ForStatement : FOR LPAREN Statement Expression SEMICOLON Statement RPAREN Block
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
    self.expr = r[2]
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
    """BreakStatement : BREAK INTL SEMICOLON
                      | BREAK SEMICOLON
    """

    def __init__(self, r):
        if len(r) == 3:
            self.count = r[1]
        else:
            self.count = 1

##
# EXPRESSIONS
##


# Priorities are listed from:
# https://en.cppreference.com/w/c/language/operator_precedence
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('left', 'LEQ', 'GEQ', 'LT', 'GT', 'EQ', 'NE'),
)


class Expression(ParserRule):
    """Expression : BinaryExpression
                  | UnaryExpression"""

    def __init__(self, r):
        self.expr = r[0]


class BinaryExpression(ParserRule):
    """BinaryExpression : Expression PLUS Expression
                        | Expression MINUS Expression
                        | Expression TIMES Expression
                        | Expression DIVIDE Expression
                        | Expression MOD Expression
                        | Expression LEQ Expression
                        | Expression GEQ Expression
                        | Expression LT Expression
                        | Expression GT Expression
                        | Expression EQ Expression
                        | Expression NE Expression
    """

    def __init__(self, r):
        self.left = r[0]
        self.right = r[2]


class UnaryExpression(ParserRule):
    """UnaryExpression : IdListR
                       | Literal
                       | FunctionCall
                       | BracketCall
                       | LPAREN Expression RPAREN
    """

    def __init__(self, r):
        if len(r) == 3:
            self.expr = r[1]
        else:
            self.expr = r[0]


class IdListR(ParserRule):
    """IdListR : ID DOT IdListR
               | ID
    """

    def __init__(self, r):
        if len(r) == 1:
            self.id = r[0]
            self.nxt = None
        else:
            self.id = r[0]
            self.nxt = r[2]


class FunctionCall(ParserRule):
    """FunctionCall : ID LPAREN ArgumentListR RPAREN
                    | ID LT TypeParameterListR GT LPAREN ArgumentListR RPAREN
    """

    def __init__(self, r):
        if len(r) == 4:
            self.name = r[0]
            self.argumentListR = r[2]
        else:
            self.name = r[0]
            self.typeParameterList = r[2]
            self.argumentListR = r[5]


class BracketCall(ParserRule):
    """BracketCall : IdListR LBRACKET Expression RBRACKET"""

    def __init__(self, r):
        self.name = r[0]
        self.expr = r[2]


class ArgumentListR(ParserRule):
    """ArgumentListR : Argument COMMA ArgumentListR
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


class Argument(ParserRule):
    """Argument : Expression"""

    def __init__(self, r):
        self.expr = r[0]


class Literal(ParserRule):
    '''Literal : IntLiteral
               | BoolLiteral
    '''

    def __init__(self, r):
        self.value = r[0]


class IntLiteral(ParserRule):
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


class BoolLiteral(ParserRule):
    '''BoolLiteral : BOOLL'''

    def __init__(self, r):
        self.value = r[0] in ('True', 'true')
