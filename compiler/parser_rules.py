import flatIR


class ParserRule:
    pass

##
# STRUCTURAL
##


class CompilationUnit(ParserRule):
    '''CompilationUnit : DefinitionListR'''

    def __init__(self, r):
        self.definitionList = r[0]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        self.definitionList.get_ir(sm, ir)


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

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        if self.nxt is not None:
            self.definition.get_ir(sm, ir)
            self.nxt.get_ir(sm, ir)


class FunctionDefinition(ParserRule):
    """FunctionDefinition : Type Id LPAREN ParameterListR RPAREN Block
    """

    def __init__(self, r):
        self.name = r[1]
        self.returnType = r[0]
        self.parameterList = r[3]
        self.block = r[5]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        ir.start_func(self.name)
        sm.begin_scope()
        ir.func().return_var = sm.get_var("return")

        self.parameterList.get_ir(sm, ir)
        self.block.get_ir(sm, ir)
        sm.end_scope()


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

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        if self.parameter is not None:
            self.parameter.get_ir(sm, ir)
        if self.nxt is not None:
            self.nxt.get_ir(sm, ir)


class Parameter(ParserRule):
    """Parameter : Type Id"""

    def __init__(self, r):
        self.type = r[0]
        self.name = r[1]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        return ir.get_var(self.name, self.type)


class Type(ParserRule):
    """Type : Id PointerListR"""

    def __init__(self, r):
        self.name = r[0]
        self.ptr_cnt = r[1].sz


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

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        sm.begin_scope()
        self.statementList.get_ir(sm, ir)
        sm.end_scope()


class StructDefinition(ParserRule):
    """StructDefinition : STRUCT Id\
            LBRACE StructMemberListR RBRACE
    """

    def __init__(self, r):
        self.typeName = r[1]
        # self.typeParameterList = r[3]
        if len(r) == 8:
            self.structMemberDeclarationList = r[6]
        else:
            self.structMemberDeclarationList = r[3]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        ir.start_struct(self.typeName)
        self.structMemberDeclarationList.get_ir(sm, ir)


class StructMemberListR(ParserRule):
    """StructMemberListR : StructMember StructMemberListR
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

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        if self.declarationStatement is not None:
            self.declarationStatement.get_ir(sm, ir)
        if self.nxt is not None:
            self.nxt.get_ir(sm, ir)


class StructMember(ParserRule):
    """StructMember : Type Id SEMICOLON"""

    def __init__(self, r):
        self.type = r[0]
        self.name = r[1]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        return
        raise NotImplementedError()

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

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        self.statement.get_ir(sm, ir)


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

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        if self.statement is not None:
            self.statement.get_ir(sm, ir)
        if self.nxt is not None:
            self.nxt.get_ir(sm, ir)


class BlankStatement(ParserRule):
    "BlankStatement : ';'"

    def __init__(self, r):
        pass

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        pass


class BlockStatement(ParserRule):
    "BlockStatement : Block"

    def __init__(self, r):
        self.block = r[0]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        sm.begin_scope()
        self.block.get_ir(sm, ir)
        sm.end_scope()


class DeclarationAssignmentStatement(ParserRule):
    """DeclarationAssignmentStatement : Type Id ASSIGNMENT\
                                        Expression SEMICOLON"""

    def __init__(self, r):
        self.type = r[0]
        self.name = r[1]
        self.expr = r[3]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        expr_var = self.expr.get_ir(sm, ir)
        decl_var = sm.get_var(self.name, self.type)
        ir.func().body.append(ir.Assignment(decl_var, expr_var))


class DeclarationFunctionCallStatement(ParserRule):
    """DeclarationFunctionCallStatement : Type FunctionCall SEMICOLON"""

    def __init__(self, r):
        self.type = r[0]
        self.funcCall = r[1]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        (name, args) = self.funcCall.get_ir(sm, ir)

        decl_var = sm.get_var(name)
        ir.func().body.append(
            ir.FunctionCallAssignment(decl_var, "__init__", args)
        )


class DeclarationStatement(ParserRule):
    """DeclarationStatement : Type Id SEMICOLON"""

    def __init__(self, r):
        self.type = r[0]
        self.name = r[1]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        decl_var = sm.get_var(self.name, self.type)
        ir.func().body.append(
            flatIR.FunctionCallAssignment(decl_var, "__init__", [])
        )


class AssignmentStatement(ParserRule):
    """AssignmentStatement : Expression ASSIGNMENT Expression SEMICOLON
                           | Expression ASSIGNMENT Expression
    """

    def __init__(self, r):
        self.name = r[0]
        self.expr = r[2]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        left = sm.get_var(self.name)
        right = self.expr.get_ir(sm, ir)
        ir.func().body.append(flatIR.Assignment(left, right))


class IfElseStatement(ParserRule):
    """IfElseStatement : IF LPAREN Expression RPAREN Block ELSE Block
    """

    def __init__(self, r):
        self.expr = r[2]
        self.blockIf = r[4]
        self.blockElse = r[6]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        self.sm.begin_scope()
        label_true = sm.new_label("if_true")
        label_true = sm.new_label("if_false")
        label_true = sm.new_label("if_end")
        e = self.expr.get_ir()
        ir.func().body.append(label_true)
        t = self.blockIf.get_ir()
        ir.func().body.append(label_false)
        f = self.blockElse.get_ir()
        ir.func().body.append(label_end)
        self.sm.end_scope()


class ForStatement(ParserRule):
    """ForStatement : FOR LPAREN Statement Expression\
            SEMICOLON Statement RPAREN Block
    """

    def __init__(self, r):
        self.statementInit = r[2]
        self.exprCheck = r[3]
        self.statementChange = r[5]
        self.block = r[7]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        self.sm.begin_scope()
        self.statementInit.get_ir()
        label_check = sm.new_label("for_check")
        label_begin = sm.new_label("for_begin")
        label_end = sm.new_label("for_end")

        ir.func().body.append(label_check)
        check = self.exprCheck.get_ir()
        ir.func.body.append(flatIR.Jump(check, label_begin, label_end))
        ir.func.body.append(label_begin)
        self.block.get_ir(sm, ir)
        self.statementChange.get_ir(sm, ir)
        ir.func.body.append(label_end)

        self.sm.end_scope()


class WhileStatement(ParserRule):
    """WhileStatement : WHILE LPAREN Expression RPAREN Block
    """

    def __init__(self, r):
        self.exprCheck = r[2]
        self.block = r[4]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        self.sm.begin_scope()
        label_check = sm.new_label("while_check")
        label_begin = sm.new_label("while_begin")
        label_end = sm.new_label("while_end")

        ir.func().body.append(label_check)
        check = self.exprCheck.get_ir()
        ir.func.body.append(flatIR.Jump(check, label_begin, label_end))
        ir.func.body.append(label_begin)
        self.block.get_ir(sm, ir)
        ir.func.body.append(label_end)

        self.sm.end_scope()


class ReturnStatement(ParserRule):
    """ReturnStatement : RETURN Expression SEMICOLON
                       | RETURN SEMICOLON
    """

    def __init__(self, r):
        if len(r) == 3:
            self.expr = r[1]
        else:
            self.expr = None

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        expr_var = self.expr.get_ir(sm, ir)
        ir.fund().body.append(flatIR.Assignment(
            sm.get_var("return"), expr_var)
        )


class BreakStatement(ParserRule):
    """BreakStatement : BREAK INTL SEMICOLON
                      | BREAK SEMICOLON
    """

    def __init__(self, r):
        if len(r) == 3:
            self.count = r[1]
        else:
            self.count = 1

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        raise NotImplementedError()

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
                  | UnaryExpression
    """

    def __init__(self, r):
        self.expr = r[0]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        return self.expr.get_ir(sm, ir)


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
                        | Expression DOT Expression

    """

    def __init__(self, r):
        self.left = r[0]
        self.op = r[1]
        self.right = r[2]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        v1 = self.left.get_ir(sm, ir)
        v2 = self.right.get_ir(sm, ir)
        dest_var = self.sm.new_tmp_var()
        ir.func_defs[-1].body.append(
            flatIR.FunctionCallAssignment(dest_var, f"__{self.op}__", [v1, v2])
        )
        return dest_var


class UnaryExpression(ParserRule):
    """UnaryExpression : Id
                       | Literal
                       | FunctionCall
                       | BracketCall
                       | LPAREN Expression RPAREN
                       | TIMES Expression
                       | AMPERSAND Expression
    """

    def __init__(self, r):
        if len(r) == 3:
            self.expr = r[1]
        else:
            self.expr = r[0]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        return self.expr.get_ir(sm, ir)



class Id(ParserRule):
    """Id : ID"""

    def __init__(self, r):
        self.id = r[0]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        raise NotImplementedError()


class FunctionCall(ParserRule):
    """FunctionCall : Id LPAREN ArgumentListR RPAREN
    """

    def __init__(self, r):
        self.name = r[0]
        self.argumentListR = r[2]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        return (self.name, self.argumentListR.get_ir(sm, ir))


class BracketCall(ParserRule):
    """BracketCall : Expression LBRACKET Expression RBRACKET"""

    def __init__(self, r):
        self.name = r[0]
        self.expr = r[2]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        raise NotImplementedError()


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

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        if self.argument is not None:
            solo = [self.argument.get_ir(sm, ir)]
        else:
            solo = []
        if self.nxt is not None:
            others = self.nxt.get_ir(sm, ir)
        else:
            others = []
        return solo+others


class Argument(ParserRule):
    """Argument : Expression"""

    def __init__(self, r):
        self.expr = r[0]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        return self.expr.get_ir(sm, ir)


class Literal(ParserRule):
    '''Literal : IntLiteral
               | BoolLiteral
    '''

    def __init__(self, r):
        self.value = r[0]

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        raise NotImplementedError()


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

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        raise NotImplementedError()


class BoolLiteral(ParserRule):
    '''BoolLiteral : BOOLL'''

    def __init__(self, r):
        self.value = r[0] in ('True', 'true')

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        raise NotImplementedError()
