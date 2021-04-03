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
        sm.begin_scope()
        for dl in self.definitionList:
            dl.fill_flat_ir(sm, definitionList)
        sm.end_scope()


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
    """StructDefinition : STRUCT ID LBRACE StructMemberListR RBRACE
                        | STRUCT ID LT TypeParameterListR GT LBRACE StructMemberListR RBRACE
    """

    def __init__(self, r):
        if len(r) == 5:
            self.typeName = r[1]
            self.structMemberList = r[3].list
            self.typeParameters = []
        else:
            self.typeName = r[1]
            self.structMemberList = r[6].list
            self.typeParameters = r[3].list

    def fill_flat_ir(self, sm: flatIR.ScopeManager, definitionList: List):
        new_struct = flatIR.StructDefinition(self.typeName)
        new_struct.members = self.structMemberList
        new_struct.typeParameters = self.typeParameters
        definitionList.append(new_struct)


class TypeParameterListR(ParserRule):
    """TypeParameterListR : ID COMMA TypeParameterListR
                          | ID
                          | empty
    """

    def __init__(self, r):
        if r[0] is None:
            self.list = []
        elif len(r) == 1:
            self.list = [r[0]]
        else:
            self.list = [r[0]]+r[1].list


class StructMember(ParserRule):
    """StructMember : Type ID SEMICOLON"""

    def __init__(self, r):
        self.type = r[0]
        self.name = r[1]


class StructMemberListR(ParserRule):
    """StructMemberListR : StructMember StructMemberListR
                         | empty
    """

    def __init__(self, r):
        if r[0] is None:
            self.list = []
        elif len(r) == 1:
            self.list = [r[0]]
        else:
            self.list = [r[0]]+r[1].list


class StructMember(ParserRule):
    """StructMember : Type ID SEMICOLON"""

    def __init__(self, r):
        self.type = r[0]
        self.name = r[1]


# Function Definitions


class FunctionDefinition(ParserRule):
    """FunctionDefinition : FN ID LPAREN ParameterListR RPAREN Block
                          | FN ID LT TypeParameterListR GT LPAREN ParameterListR RPAREN Block
    """

    def __init__(self, r):
        if len(r) == 6:
            self.name = r[1]
            self.parameterList = r[3].list
            self.typeParameterList = []
            self.block = r[5]
        else:
            self.name = r[1]
            self.parameterList = r[6].list
            self.typeParameterList = r[3].list
            self.block = r[8]

    def fill_flat_ir(self, sm: flatIR.ScopeManager, definitionList: List):
        new_func = flatIR.FunctionDefinition(self.name)
        sm.begin_scope()
        sm.new_var_name("return")

        new_func.body.append(flatIR.Description(
            "Starting parameter stack shifting"))
        new_func.parameters = self.parameterList
        new_func.typeParameters = self.typeParameterList
        for par in self.parameterList:
            parptr = sm.new_var_name(par.name)
            new_func.body.append(flatIR.StackAllocate(parptr, par.type))
            new_func.body.append(flatIR.StoreValueToPointer(parptr, par.name))
        new_func.body.append(flatIR.Description(
            "Ending parameter stack shifting"))

        self.block.fill_flat_ir(sm, new_func, new_sc=False)

        sm.end_scope()
        definitionList.append(new_func)


class ParameterListR(ParserRule):
    """ParameterListR : Parameter COMMA ParameterListR
                      | Parameter
                      | empty
    """

    def __init__(self, r):
        if r[0] is None:
            self.list = []
        elif len(r) == 1:
            self.list = [r[0]]
        else:
            self.list = [r[0]]+r[2].list


class Parameter(ParserRule):
    """Parameter : Type ID"""

    def __init__(self, r):
        self.type = r[0]
        self.name = r[1]


class Type(ParserRule):
    """Type : ID PointerListR
            | ID LT TypeArgumentListR GT PointerListR"""

    def __init__(self, r):
        if len(r) == 2:
            self.name = r[0]
            self.typeArgumentList = []
            self.ptr_cnt = r[1].sz
        else:
            self.name = r[0]
            self.typeArgumentList = r[2].list
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
        self.statementList = r[1].list

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
                 | InitStatement
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
        if isinstance(self.statement, Expression):
            self.statement.fill_flat_ir(sm, func, ptr=False)
        else:
            self.statement.fill_flat_ir(sm, func)


class StatementListR(ParserRule):
    """StatementListR : Statement StatementListR
                      | empty
    """

    def __init__(self, r):
        if len(r) == 1:
            self.list = []
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
    """InitStatement : LET ID ASSIGNMENT\
                                        InitCall SEMICOLON"""

    def __init__(self, r):
        self.name = r[1]
        self.initExpression = r[3]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):

        # this name will contain a ptr to stack
        uniqn = sm.new_var_name(self.name)
        init = self.initExpression.fill_flat_ir(sm, func)
        func.body.append(flatIR.Assignment(uniqn, init))


class InitCall(ParserRule):
    """InitCall : ID LBRACE ArgumentListR RBRACE
                | ID LT TypeArgumentListR GT LBRACE ArgumentListR RBRACE"""

    def __init__(self, r):
        if len(r) == 4:
            self.type = r[0]
            self.typeArgumentList = []
            self.argumentList = r[2].list
        else:
            self.type = r[0]
            self.typeArgumentList = r[2].list
            self.argumentList = r[5].list

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):

        # this name will contain a ptr to stack
        uniqn = sm.new_tmp_var_name()
        func.body.append(flatIR.StackAllocate(uniqn, self.type))

        args = [a.fill_flat_ir(sm, func) for a in self.argumentList]
        tmp = sm.new_tmp_var_name()
        func.body.append(flatIR.FunctionCall(tmp, "__init__",
                                             [uniqn] +
                                             args,
                                             self.typeArgumentList
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
        func.body.append(flatIR.JumpToLabel(el))

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
        func.body.append(flatIR.JumpToLabel(fs))

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
        func.body.append(flatIR.JumpToLabel(ws))

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
                  | IdExpression
    """

    def __init__(self, r):
        self.expr = r[0]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition, ptr):
        return self.expr.fill_flat_ir(sm, func, ptr)


class BinaryExpressionClassic(ParserRule):
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
    op_mapping = {
        "+": "add",
        "-": "sub",
        "*": "mul",
        "/": "div",
        "%": "mod",
        "<=": "leq",
        ">=": "geq",
        "<": "lt",
        ">": "gt",
        "==": "eq",
        "!=": "ne",
    }

    def __init__(self, r):
        self.left = r[0]
        self.op = f"__{self.op_mapping[r[1]]}__"
        self.right = r[2]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition, ptr):

        if ptr:
            raise RuntimeError("cant acquire lvalue")
        left = self.left.fill_flat_ir(sm, func, ptr=False)
        right = self.right.fill_flat_ir(sm, func, ptr=False)
        tmp = sm.new_tmp_var_name(self.op.lower())
        func.body.append(flatIR.FunctionCall(
            tmp, self.op, [left, right], []))
        return tmp


class UnaryExpression(ParserRule):
    """UnaryExpression : Literal
                       | FunctionCall
                       | BracketCall
                       | InitCall
                       | LPAREN Expression RPAREN
                       | DereferenceExpression
                       | AddressExpression
    """

    def __init__(self, r):
        if len(r) == 3:
            self.expr = r[1]
        else:
            self.expr = r[0]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition, ptr):
        return self.expr.fill_flat_ir(sm, func, ptr)


class FunctionCall(ParserRule):
    """FunctionCall : ID LPAREN ArgumentListR RPAREN
                    | ID LT TypeArgumentListR GT LPAREN ArgumentListR RPAREN
    """

    def __init__(self, r):
        if len(r) == 4:
            self.name = r[0]
            self.argumentList = r[2].list
            self.typeArgumentList = []
        else:
            self.name = r[0]
            self.argumentList = r[5].list
            self.typeArgumentList = r[2].list

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition, ptr):
        if ptr:
            raise RuntimeError()

        tmp = sm.new_tmp_var_name()
        args = [a.fill_flat_ir(sm, func) for a in self.argumentList]
        func.body.append(flatIR.FunctionCall(
            tmp, self.name, args, self.typeArgumentList))
        return tmp


class TypeArgumentListR(ParserRule):
    """TypeArgumentListR : Type COMMA TypeArgumentListR
                         | Type
                         | empty
    """

    def __init__(self, r):
        if r[0] is None:
            self.list = []
        elif len(r) == 1:
            self.list = [r[0]]
        else:
            self.list = [r[0]] + r[2].list


class IdExpression(ParserRule):
    """IdExpression : ID
                    | IdExpression DOT ID
    """

    def __init__(self, r):
        if len(r) == 3:
            self.nxt = r[0]
            self.id = r[2]
        else:
            self.nxt = None
            self.id = r[0]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition, ptr):
        if self.nxt is None:
            tar = sm.get_var_name(self.id)
        else:
            prev = self.nxt.fill_flat_ir(sm, func, ptr=True)
            tar = sm.new_tmp_var_name()
            func.body.append(flatIR.GetElementPtr(tar, prev, self.id))

        if ptr:
            return tar
        else:
            tar2 = sm.new_tmp_var_name()
            func.body.append(flatIR.LoadValueFromPointer(tar2, tar))
            return tar2


class BracketCall(ParserRule):
    """BracketCall : Expression LBRACKET Expression RBRACKET"""

    def __init__(self, r):
        self.name = r[0]
        self.expr = r[2]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition, ptr):
        container = self.name.fill_flat_ir(sm, func, ptr=True)
        offset = self.name.fill_flat_ir(sm, func, ptr=False)
        new = sm.new_tmp_var_name()
        func.body.append(flatIR.GetPointerOffset(new, container, offset))
        if ptr:
            return new
        else:
            new_val = sm.new_tmp_var_name()
            func.body.append(flatIR.LoadValueFromPointer(new_val, new))
            return new_val


class ArgumentListR(ParserRule):
    """ArgumentListR : Argument COMMA ArgumentListR
                     | Argument
                     | empty
    """

    def __init__(self, r):
        if r[0] is None:
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
        return self.expr.fill_flat_ir(sm, func, ptr=False)


class DereferenceExpression(ParserRule):
    """DereferenceExpression : TIMES Expression"""

    def __init__(self, r):
        self.expr = r[1]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition, ptr):
        orig = self.expr.fill_flat_ir(sm, func, ptr)
        new = sm.new_tmp_var_name()
        func.body.append(flatIR.LoadValueFromPointer(new, orig))


class AddressExpression(ParserRule):
    """AddressExpression : AMPERSAND Expression"""

    def __init__(self, r):
        self.expr = r[1]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition, ptr):
        if ptr:
            raise RuntimeError("")
        orig = self.expr.fill_flat_ir(sm, func, ptr=True)
        return orig


class Literal(ParserRule):
    '''Literal : IntLiteral
               | BoolLiteral
    '''

    def __init__(self, r):
        self.value = r[0]

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition, ptr):
        if ptr:
            raise RuntimeError("Cant get lvalue to a literal")
        else:
            return self.value.fill_flat_ir(sm, func)


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
        tmp = sm.new_tmp_var_name()
        func.body.append(flatIR.IntConstant(
            tmp, self.value, self.size, self.signed))
        return tmp


class BoolLiteral(ParserRule):
    '''BoolLiteral : BOOLL'''

    def __init__(self, r):
        self.value = r[0] in ('True', 'true')

    def fill_flat_ir(self, sm: flatIR.ScopeManager,
                     func: flatIR.FunctionDefinition):
        tmp = sm.new_tmp_var_name()
        func.body.append(flatIR.BoolConstant(tmp, self.value))
        return tmp
