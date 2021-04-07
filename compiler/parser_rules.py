from parser import SemanticEnvironment as SE
from parser import SemanticStatus as SS
import lang_ast as la


class ParserRule:
    pass


class CompilationUnit(ParserRule):
    '''CompilationUnit : DefinitionList'''

    def __init__(self, r):
        self.definitionList = r[0]

    def parse_semantics(self, se: SE):
        return la.Program(
            [d.parse_semantics(se) for d in self.definitionList.flist],
            [d.parse_semantics(se) for d in self.definitionList.slist]
        )


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
        self.expr = r[1]
        self.block = r[2]

    def parse_semantics(self, se: SE):
        se.add(SS.STRUCT)
        sl = self.block.parse_semantics(se)
        se.pop()
        if hasattr(self.expr.expr, "id"):
            return la.StructDefinition(
                name=self.expr.expr.id,
                type_parameter_names=[],
                block=la.Block(sl)
            )
        else:
            return la.StructDefinition(
                name=self.expr.expr.expr.expr.expr.id,
                type_parameter_names=[
                    i.expr.id for i in self.expr.expr.expr.expr_list],
                block=la.Block(sl)
            )


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

    def parse_semantics(self, se: SE):
        se.add(SS.FUNC)
        sl = self.block.parse_semantics(se)
        se.pop()
        se.add(SS.TYPE_EXPR)
        if self.expr_ret is not None:
            expr_ret = self.expr_ret.parse_semantics(se)
        else:
            expr_ret = "void"
        se.pop()
        pce = self.expr.expr.expr
        if hasattr(pce.expr.expr, "id"):
            name = pce.expr.expr.id
            type_parameter_names = []
            parameters = [[e.expr.id1, e.expr.id2] for e in pce.expr_list]
        else:
            name = pce.expr.expr.expr.expr.expr.id
            type_parameter_names = [
                e.expr.id for e in pce.expr.expr.expr.expr_list]
            parameters = [[e.expr.id1, e.expr.id2] for e in pce.expr_list]
        res = la.FunctionDefinition(name, type_parameter_names,
                                     parameters, expr_ret, la.Block(sl))
        return res


class Block(ParserRule):
    "Block : LBRACE StatementList RBRACE"

    def __init__(self, r):
        self.statementList = r[1].list

    def parse_semantics(self, se: SE):
        return [s.parse_semantics(se) for s in self.statementList]


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

    def parse_semantics(self, se: SE):
        return self.statement.parse_semantics(se)


class ExpressionStatement(ParserRule):
    """ExpressionStatement : Expression SEMICOLON"""

    def __init__(self, r):
        self.expr = r[0]

    def parse_semantics(self, se: SE):
        if se.top() != SS.FUNC:
            raise RuntimeError("Cant parse expression out of func!")
        se.add(SS.RUNTIME_EXPR)
        a = self.expr.parse_semantics(se)
        se.pop()
        return a


class DeclarationStatement(ParserRule):
    """DeclarationStatement : Expression Expression SEMICOLON"""

    def __init__(self, r):
        self.expr1 = r[0]
        self.expr2 = r[1]

    def parse_semantics(self, se: SE):
        if se.top() != SS.STRUCT:
            raise RuntimeError("Cant declare memeber out of struct!")
        name = self.expr2.expr.id
        se.add(SS.TYPE_EXPR)
        a = self.expr1.parse_semantics(se)
        se.pop()
        return la.MemberDeclarationStatement(a, name)


class TypeStatement(ParserRule):
    """TypeStatement : TYPE Expression ASSIGNMENT Expression SEMICOLON"""

    def __init__(self, r):
        self.left = r[1]
        self.right = r[3]

    def parse_semantics(self, se: SE):
        name = self.left.expr.id
        se.add(SS.TYPE_EXPR)
        a = self.right.parse_semantics(se)
        se.pop()
        return la.TypeDeclarationStatement(a, name)


class BlankStatement(ParserRule):
    "BlankStatement : SEMICOLON"

    def __init__(self, r):
        pass

    def parse_semantics(self, se: SE):
        return la.BlankStatement()


class BlockStatement(ParserRule):
    "BlockStatement : Block"

    def __init__(self, r):
        self.block = r[0]

    def parse_semantics(self, se: SE):
        if se.top() != SS.FUNC:
            raise RuntimeError("Cant declare new block out of func!")
        a = self.block.parse_semantics(se)
        return la.BlockStatement(a)


class InitStatement(ParserRule):
    """InitStatement : LET Expression ASSIGNMENT Expression SEMICOLON
    """

    def __init__(self, r):
        self.name = r[1]
        self.expr = r[3]

    def parse_semantics(self, se: SE):
        if se.top() != SS.FUNC:
            name = self.name.expr.id
            se.add(SS.TYPE_EXPR)
            a = self.expr.parse_semantics(se)
            se.pop()
            return la.MemberDeclarationStatement(name, a)
        else:
            name = self.name.expr.id
            se.add(SS.RUNTIME_EXPR)
            a = self.expr.parse_semantics(se)
            se.pop()
            return la.InitStatement(name, a)


class AssignmentStatement(ParserRule):
    """AssignmentStatement : Expression ASSIGNMENT Expression SEMICOLON
    """

    def __init__(self, r):
        self.left = r[0]
        self.right = r[2]

    def parse_semantics(self, se: SE):
        if se.top() != SS.FUNC:
            raise RuntimeError("Cant assign to a var out of func!")
        se.add(SS.RUNTIME_EXPR)
        l = self.left.parse_semantics(se)
        r = self.right.parse_semantics(se)
        se.pop()
        return la.AssignmentStatement(l, r)


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

    def parse_semantics(self, se: SE):
        if se.top() != SS.FUNC:
            raise RuntimeError("Cant use if/else out of func!")
        se.add(SS.RUNTIME_EXPR)
        a = self.expr.parse_semantics(se)
        if self.blockElse is None:
            res = la.IfElseStatement(
                a,
                self.blockIf.parse_semantics(se),
                la.Block([])
            )
        else:
            res = la.IfElseStatement(
                a,
                self.blockIf.parse_semantics(se),
                self.blockElse.parse_semantics(se),
            )
        se.pop()
        return res


class ForStatement(ParserRule):
    """ForStatement : FOR LPAREN Statement Expression\
            SEMICOLON Statement RPAREN Block
    """

    def __init__(self, r):
        self.statementInit = r[2]
        self.exprCheck = r[3]
        self.statementChange = r[5]
        self.block = r[7]

    def parse_semantics(self, se: SE):
        if se.top() != SS.FUNC:
            raise RuntimeError("Cant use for out of func!")
        se.add(SS.RUNTIME_EXPR)
        res = la.ForStatement(
            self.statementInit.parse_semantics(se),
            self.exprCheck.parse_semantics(se),
            self.statementChange.parse_semantics(se),
            self.block.parse_semantics(se)
        )
        se.pop()
        return res


class WhileStatement(ParserRule):
    """WhileStatement : WHILE LPAREN Expression RPAREN Block
    """

    def __init__(self, r):
        self.exprCheck = r[2]
        self.block = r[4]

    def parse_semantics(self, se: SE):
        if se.top() != SS.FUNC:
            raise RuntimeError("Cant use while out of func!")
        se.add(SS.RUNTIME_EXPR)
        res = la.WhileStatement(
            self.exprCheck.parse_semantics(se),
            self.block.parse_semantics(se)
        )
        se.pop()
        return res


class ReturnStatement(ParserRule):
    """ReturnStatement : RETURN Expression SEMICOLON
                       | RETURN SEMICOLON
    """

    def __init__(self, r):
        if len(r) == 3:
            self.expr = r[1]
        else:
            self.expr = None

    def parse_semantics(self, se: SE):
        if se.top() != SS.FUNC:
            raise RuntimeError("Cant use return out of func!")
        if self.expr is None:
            return la.ReturnStatement(None)
        else:
            se.add(SS.RUNTIME_EXPR)
            e = self.expr.parse_semantics(se)
            se.pop()
            return la.ReturnStatement(e)


class BreakStatement(ParserRule):
    """BreakStatement : BREAK IntLiteral SEMICOLON
                      | BREAK SEMICOLON
    """

    def __init__(self, r):
        if len(r) == 3:
            self.count = r[1].value
        else:
            self.count = 1

    def parse_semantics(self, se: SE):
        if se.top() != SS.FUNC:
            raise RuntimeError("Cant use return out of func!")


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
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('left', 'LEQ', 'GEQ', 'LT', 'GT', 'EQ', 'NE'),
    ('left', 'DOT', 'DEREF'),
    ('right', 'ADDRESS'),
    ('left', 'LPAREN', 'LBRACE')
)


class Expression(ParserRule):
    """Expression : BinaryExpression
                  | UnaryExpression
                  | IdExpression
                  | IdPairExpression
    """

    def __init__(self, r):
        self.expr = r[0]

    def parse_semantics(self, se: SE):
        return self.expr.parse_semantics(se)


class IdExpression(ParserRule):
    """IdExpression : ID"""

    def __init__(self, r):
        self.id = r[0]

    def parse_semantics(self, se: SE):
        return self.id


class IdPairExpression(ParserRule):
    """IdPairExpression : ID ID"""

    def __init__(self, r):
        self.id1 = r[0]
        self.id2 = r[1]

    def parse_semantics(self, se: SE):
        raise RuntimeError("IdPair should not be parsed directly!")


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
        self.op = r[1]
        self.right = r[2]

    def parse_semantics(self, se: SE):
        if se.top() == SS.TYPE_EXPR:
            return la.TypeBinaryExpression(
                self.left.parse_semantics(se),
                self.op,
                self.right.parse_semantics(se)
            )
        if se.top() == SS.RUNTIME_EXPR:
            return la.BinaryExpression(
                self.left.parse_semantics(se),
                self.op,
                self.right.parse_semantics(se)
            )
        raise RuntimeError("Shouldn't have gotten here!")


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

    def parse_semantics(self, se: SE):
        return self.expr.parse_semantics(se)


class ParenthesesExpression(ParserRule):
    """ParenthesesExpression : LPAREN Expression RPAREN"""

    def __init__(self, r):
        self.expr = r[1]

    def parse_semantics(self, se: SE):
        return self.expr.parse_semantics(se)


class AngleCallExpression(ParserRule):
    """AngleCallExpression : Expression LANGLE ExpressionList RANGLE"""

    def __init__(self, r):
        self.expr = r[0]
        self.expr_list = r[2].list

    def parse_semantics(self, se: SE):
        if se.top() != SS.TYPE_EXPR:
            raise RuntimeError("Angle call is a part of type expression!")
        return la.TypeAngleExpression(
            self.expr.parse_semantics(se),
            [s.parse_semantics(se) for s in self.expr_list]
        )


class ParenthesesCallExpression(ParserRule):
    """ParenthesesCallExpression : Expression LPAREN\
            ExpressionList RPAREN"""

    def __init__(self, r):
        self.expr = r[0]
        self.expr_list = r[2].list

    def parse_semantics(self, se: SE):
        if se.top() != SS.RUNTIME_EXPR:
            raise RuntimeError("Parentheses call is\
                    a part of runtime expression!")
        if hasattr(self.expr.expr, "id"):
            name = self.expr.expr.id
            type_expr = []
            se.add(SS.RUNTIME_EXPR)
            args = [e.parse_semantics(se) for e in self.expr_list]
            se.pop()
        else:
            name = self.expr.expr.expr.expr.expr.id
            se.add(SS.TYPE_EXPR)
            type_expr = [e.parse_semantics(se) for
                         e in self.expr.expr.expr.expr_list]
            se.pop()
            se.add(SS.RUNTIME_EXPR)
            args = [e.parse_semantics(se) for e in self.expr_list]
            se.pop()

        return la.CallExpression(name, type_expr, args)


class DotExpression(ParserRule):
    """DotExpression : Expression DOT Expression
    """

    def __init__(self, r):
        self.left = r[0]
        self.right = r[2]

    def parse_semantics(self, se: SE):
        if se.top() == SS.RUNTIME_EXPR:
            return la.MemberIndexExpression(
                self.left.parse_semantics(se),
                self.right.expr.id
            )
        if se.top() == SS.TYPE_EXPR:
            return la.TypeMemberIndexExpression(
                self.left.parse_semantics(se),
                self.right.expr.id
            )


class BracketCallExpression(ParserRule):
    """BracketCallExpression : Expression LBRACKET Expression\
            RBRACKET"""

    def __init__(self, r):
        self.expr1 = r[0]
        self.expr2 = r[2]

    def parse_semantics(self, se: SE):
        if se.top() != SS.RUNTIME_EXPR:
            raise RuntimeError("Bracket call not available in typeexpr")
        e1 = self.expr1.parse_semantics(se)
        e2 = self.expr1.parse_semantics(se)
        return la.BracketCallExpression(e1, e2)


class DereferenceExpression(ParserRule):
    """DereferenceExpression : Expression DEREF"""

    def __init__(self, r):
        self.expr = r[0]

    def parse_semantics(self, se: SE):
        if se.top() == SS.RUNTIME_EXPR:
            e = self.expr.parse_semantics(se)
            return la.DerefExpression(e)
        if se.top() == SS.TYPE_EXPR:
            e = self.expr.parse_semantics(se)
            return la.TypeDerefExpression(e)


class AddressExpression(ParserRule):
    """AddressExpression : ADDRESS Expression"""

    def __init__(self, r):
        self.expr = r[1]

    def parse_semantics(self, se: SE):
        if se.top() == SS.RUNTIME_EXPR:
            e = self.expr.parse_semantics(se)
            return la.AddressExpression(e)
        if se.top() == SS.TYPE_EXPR:
            e = self.expr.parse_semantics(se)
            return la.TypePtrExpression(e)


class LiteralExpression(ParserRule):
    '''LiteralExpression : IntLiteral
                         | BoolLiteral
    '''

    def __init__(self, r):
        self.value = r[0]

    def parse_semantics(self, se: SE):
        if se.top() != SS.RUNTIME_EXPR:
            raise RuntimeError("literals can only be runtime")
        return self.value.parse_semantics(se)


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

    def parse_semantics(self, se: SE):
        return la.IntLiteralExpression(self.value, self.signed, self.size)


class BoolLiteral(ParserRule):
    '''BoolLiteral : BOOLL'''

    def __init__(self, r):
        self.value = r[0] in ('True', 'true')

    def parse_semantics(self, se: SE):
        return la.BoolLiteralExpression(self.value)
