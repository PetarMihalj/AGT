import flatIR
from typing import List


class ParserRule:
    pass

##
# STRUCTURAL
##


class CompilationUnit(ParserRule):
    '''CompilationUnit : DefinitionListR'''

    def __init__(self, r):
        self.definitionList = r[0].list

    def fill_flat_ir(self, sm: flatIR.ScopeManager, definitionList: List):
        for dl in self.definitionList:
            dl.fill_flat_ir(sm, definitionList)


class DefinitionListR(ParserRule):
    """DefinitionListR : FunctionDefinition DefinitionListR
                       | StructDefinition DefinitionListR
                       | empty
    """

    def __init__(self, r):
        if len(r) == 1:
            self.list = []
        else:
            self.list = [r[0]]+r[1].list


# Structs


class StructDefinition(ParserRule):
    """StructDefinition : STRUCT Id LBRACE StructMemberListR RBRACE
    """

    def __init__(self, r):
        self.typeName = r[1]
        self.structMemberList = r[3].list

    def fill_flat_ir(self, sm: flatIR.ScopeManager, definitionList: List):
        new_struct = flatIR.StructDefinition(self.typeName)
        new_struct.members = self.structMemberList
        definitionList.append(new_struct)


class StructMemberListR(ParserRule):
    """StructMemberListR : StructMember StructMemberListR
                         | empty
    """

    def __init__(self, r):
        if r[0] == 'empty':
            self.list = []
        elif len(r) == 1:
            self.list = [r[0]]
        else:
            self.list = [r[0]]+r[1].list


class StructMember(ParserRule):
    """StructMember : Type Id SEMICOLON"""

    def __init__(self, r):
        self.type = r[0]
        self.name = r[1]


# Function Definitions


class FunctionDefinition(ParserRule):
    """FunctionDefinition : Type Id LPAREN ParameterListR RPAREN Block
    """

    def __init__(self, r):
        self.name = r[1]
        self.returnType = r[0]
        self.parameterList = r[3].list
        self.templateParameterList = []
        self.block = r[5]

    def fill_flat_ir(self, sm: flatIR.ScopeManager, definitionList: List):
        new_func = flatIR.FunctionDefinition(self.name)
        sm.begin_scope()

        new_func.parameters = self.parameterList
        new_func.returnType = self.returnType

        self.block.fill_flat_ir(sm, new_func, new_sc=False)

        sm.end_scope()
        definitionList.append(new_func)


class ParameterListR(ParserRule):
    """ParameterListR : Parameter COMMA ParameterListR
                      | Parameter
                      | empty
    """

    def __init__(self, r):
        if r[0] == 'empty':
            self.list = []
        elif len(r) == 1:
            self.list = [r[0]]
        else:
            self.list = [r[0]]+r[2].list


class Parameter(ParserRule):
    """Parameter : Type Id"""

    def __init__(self, r):
        self.type = r[0]
        self.name = r[1]


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

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition, new_sc=True):
        if new_sc:
            sm.begin_scope()
        for stat in self.statementList:
            stat.fill_flat_ir(sm, func)
        if new_sc:
            sm.end_scope()


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

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        self.statement.fill_flat_ir(sm, func)


class StatementListR(ParserRule):
    """StatementListR : Statement StatementListR
                      | empty
    """

    def __init__(self, r):
        if len(r) == 1:
            self.list = [r[0]]
        else:
            self.list = [r[0]]+r[1].list


class BlankStatement(ParserRule):
    "BlankStatement : ';'"

    def __init__(self, r):
        pass

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        pass


class BlockStatement(ParserRule):
    "BlockStatement : Block"

    def __init__(self, r):
        self.block = r[0]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        self.block.fill_flat_ir(sm, func)


class InitStatement(ParserRule):
    """InitializationStatement : LET Id ASSIGNMENT\
                                        InitCall SEMICOLON"""

    def __init__(self, r):
        self.name = r[1]
        self.initExpression = r[3]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):

        # this name will contain a ptr to stack
        uniqn = sm.new_var_name(self.name)
        init = self.initExpression.fill_flat_ir(sm, func)
        self.body.append(flatIR.Assignment(uniqn, init))


class InitCall(ParserRule):
    """InitCall : Id LBRACE ArgumentListR RBRACE"""

    def __init__(self, r):
        self.name = r[0]
        self.argumentList = r[2]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):

        # this name will contain a ptr to stack
        uniqn = sm.new_tmp_var_name()
        func.body.append(flatIR.StackAllocate(uniqn, self.type))

        tmp = sm.new_tmp_var_name()
        self.body.append(flatIR.FunctionCall(tmp, "__init__",
                                             [uniqn] +
                                             self.argumentListR,
                                             []
                                             ))
        return tmp


class AssignmentStatement(ParserRule):
    """AssignmentStatement : Expression ASSIGNMENT Expression SEMICOLON
                           | Expression ASSIGNMENT Expression
    """

    def __init__(self, r):
        self.left = r[0]
        self.right = r[2]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        right = self.right.fill_flat_ir(sm, func, ptr=False)
        left = self.left.fill_flat_ir(sm, func, ptr=True)
        func.body.append(flatIR.StoreValueToPointer(left, right))


class IfElseStatement(ParserRule):
    """IfElseStatement : IF LPAREN Expression RPAREN Block ELSE Block
    """

    def __init__(self, r):
        self.expr = r[2]
        self.blockIf = r[4]
        self.blockElse = r[6]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        tl = sm.new_label_name("if_true")
        fl = sm.new_label_name("if_false")
        el = sm.new_label_name("if_end")

        e = self.expr.fill_flat_ir(sm, func, ptr=False)
        func.body.append(flatIR.JumpToLabelTrue(e, tl))

        func.body.append(flatIR.Label(fl))
        self.blockIf.fill_flat_ir(sm, func)
        self.body.append(flatIR.JumpToLabel(el))

        func.body.append(flatIR.Label(tl))
        self.blockElse.fill_flat_ir(sm, func)

        func.body.append(el)


class ForStatement(ParserRule):
    """ForStatement : FOR LPAREN Statement Expression\
            SEMICOLON Statement RPAREN Block
    """

    def __init__(self, r):
        self.statementInit = r[2]
        self.exprCheck = r[3]
        self.statementChange = r[5]
        self.block = r[7]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        self.sm.begin_scope()

        fs = sm.new_label_name("for_start")
        fe = sm.new_label_name("for_end")
        self.sm.break_label_stack.append(fe)

        self.statementInit.fill_flat_ir(sm, func)
        func.body.append(flatIR.Label(fs))
        e = self.exprCheck.fill_flat_ir(sm, func, ptr=False)
        func.body.append(flatIR.JumpToLabelFalse(e, fe))

        self.block.fill_flat_ir(sm, func)
        self.statementChange.fill_flat_ir(sm, func)
        self.body.append(flatIR.JumpToLabel(fs))

        func.body.append(flatIR.Label(fe))

        self.sm.break_label_stack.pop_back()
        self.sm.end_scope()


class WhileStatement(ParserRule):
    """WhileStatement : WHILE LPAREN Expression RPAREN Block
    """

    def __init__(self, r):
        self.exprCheck = r[2]
        self.block = r[4]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        self.sm.begin_scope()

        ws = sm.new_label_name("while_start")
        we = sm.new_label_name("while_end")
        self.sm.break_label_stack.append(we)

        func.body.append(flatIR.Label(ws))
        e = self.exprCheck.fill_flat_ir(sm, func, ptr=False)
        func.body.append(flatIR.JumpToLabelFalse(e, we))

        self.block.fill_flat_ir(sm, func)
        self.body.append(flatIR.JumpToLabel(ws))

        func.body.append(flatIR.Label(we))

        self.sm.break_label_stack.pop_back()
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

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        a = self.expr.fill_flat_ir(sm, func, ptr=False)
        ret = sm.get_var_name("return")
        func.body.append(flatIR.StoreValueToPointer(ret, a))


class BreakStatement(ParserRule):
    """BreakStatement : BREAK INTL SEMICOLON
                      | BREAK SEMICOLON
    """

    def __init__(self, r):
        if len(r) == 3:
            self.count = r[1]
        else:
            self.count = 1

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        func.body.append(flatIR.JumpToLabel(sm.break_label_stack[-self.count]))

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

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        pass

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

    """

    def __init__(self, r):
        self.left = r[0]
        self.op = r[1]
        self.right = r[2]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        pass

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

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        pass

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        return self.expr.get_ir(sm, ir)


class Id(ParserRule):
    """Id : ID"""

    def __init__(self, r):
        self.id = r[0]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        pass

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        raise NotImplementedError()


class FunctionCall(ParserRule):
    """FunctionCall : Id LPAREN ArgumentListR RPAREN
    """

    def __init__(self, r):
        self.name = r[0]
        self.argumentList = r[2]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):

        tmp = sm.new_tmp_var_name()
        args = [a.fill_flat_ir() for a in self.argumentList]
        func.body.append(flatIR.FunctionCall(tmp, self.name, args, []))
        return tmp


class BracketCall(ParserRule):
    """BracketCall : Expression LBRACKET Expression RBRACKET"""

    def __init__(self, r):
        self.name = r[0]
        self.expr = r[2]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        pass

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        raise NotImplementedError()


class ArgumentListR(ParserRule):
    """ArgumentListR : Argument COMMA ArgumentListR
                     | Argument
                     | empty
    """

    def __init__(self, r):
        if r[0] == 'empty':
            self.list = []
        elif len(r) == 1:
            self.list = [r[0]]
        else:
            self.list = [r[0]] + r[2].list


class Argument(ParserRule):
    """Argument : Expression"""

    def __init__(self, r):
        self.expr = r[0]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        pass


class Literal(ParserRule):
    '''Literal : IntLiteral
               | BoolLiteral
    '''

    def __init__(self, r):
        self.value = r[0]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        pass

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

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        pass

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        raise NotImplementedError()


class BoolLiteral(ParserRule):
    '''BoolLiteral : BOOLL'''

    def __init__(self, r):
        self.value = r[0] in ('True', 'true')

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        pass

    def get_ir(self, sm: flatIR.ScopeManager, ir: flatIR.FlatIR):
        raise NotImplementedError()
