from dataclasses import dataclass
from typing import List, Tuple, Union, Any
from enum import Enum
import sys

from ..helpers import add_method_parse_semantics
from ..helpers import tree_print
from ..syntax_parsing import parser_rules as pr

NoneType = type(None)

class Structural:
    pass


class FunctionStatement:
    def __init__(self):
        self.linespan = (-1,-1)
        self.lexspan = (-1,-1)

class StructStatement:
    def __init__(self):
        self.linespan = (-1,-1)
        self.lexspan = (-1,-1)

class ValueExpression:
    def __init__(self):
        self.linespan = (-1,-1)
        self.lexspan = (-1,-1)

class TypeExpression:
    def __init__(self):
        self.linespan = (-1,-1)
        self.lexspan = (-1,-1)


@dataclass
class Program(Structural):
    function_definitions: List['FunctionDefinition']
    struct_definitions: List['StructDefinition']


@dataclass
class FunctionDefinition(Structural):
    name: str
    type_parameter_names: List[str]
    parameter_names: List[str]
    expr_ret: TypeExpression
    statement_list: List[FunctionStatement]


@ dataclass
class StructDefinition(Structural):
    name: str
    type_parameter_names: List[str]
    statement_list: List[StructStatement]

# function statement

@ dataclass
class BlockStatement(FunctionStatement):
    statement_list: List[FunctionStatement]


@ dataclass
class ExpressionStatement(FunctionStatement):
    "valueexpr;"
    expr: ValueExpression
    def __post_init__(self):
        super().__init__()

@ dataclass
class TypeDeclarationStatementFunction(FunctionStatement):
    "type a = typeexpr"
    name: str
    type_expr: TypeExpression

    def __post_init__(self):
        super().__init__()

@ dataclass
class AssignmentStatement(FunctionStatement):
    "valueexpr = valueexpr"
    left: ValueExpression
    right: ValueExpression

@ dataclass
class InitStatement(FunctionStatement):
    "let a = valueexpr"
    name: str
    expr: ValueExpression

@ dataclass
class WhileStatement(FunctionStatement):
    expr_check: ValueExpression
    statement_list: List[FunctionStatement]


@ dataclass
class ForStatement(FunctionStatement):
    stat_init: FunctionStatement
    expr_check: ValueExpression
    stat_change: FunctionStatement
    statement_list: List[FunctionStatement]


@ dataclass
class IfElseStatement(FunctionStatement):
    expr: ValueExpression
    statement_list_true: List[FunctionStatement]
    statement_list_false: List[FunctionStatement]


@ dataclass
class ReturnStatement(FunctionStatement):
    expr: Union[ValueExpression, NoneType]


@ dataclass
class BreakStatement(FunctionStatement):
    no: int

# struct statements

@ dataclass
class MemberDeclarationStatement(StructStatement):
    "let a = typeexpr"
    name: str
    type_expr: TypeExpression

@ dataclass
class TypeDeclarationStatementStruct(StructStatement):
    "type a = typeexpr"
    name: str
    type_expr: TypeExpression

# Value expressions

@ dataclass
class IdExpression(ValueExpression):
    name: str

@ dataclass
class BinaryExpression(ValueExpression):
    left: ValueExpression
    op: str
    right: ValueExpression


@ dataclass
class BracketCallExpression(ValueExpression):
    expr: ValueExpression
    index: ValueExpression


@ dataclass
class MemberIndexExpression(ValueExpression):
    expr: ValueExpression
    member: str


@ dataclass
class DerefExpression(ValueExpression):
    expr: ValueExpression


@ dataclass
class AddressExpression(ValueExpression):
    expr: ValueExpression


@ dataclass
class IntLiteralExpression(ValueExpression):
    value: int
    size: int


@ dataclass
class BoolLiteralExpression(ValueExpression):
    value: bool


@ dataclass
class CallExpression(ValueExpression):
    name: str
    type_expr_list: List[TypeExpression]
    args: List[ValueExpression]

# Type Expressions

ops_mapping = {
        '==': '__eq__',
        '!=': '__ne__',
        '>': '__gt__',
        '<': '__lt__',
        '<=': '__le__',
        '>=': '__ge__',

        '+': '__add__',
        '-': '__sub__',
        '/': '__div__',
        '*': '__mul__',
        '%' : ' __mod__',
}


@ dataclass
class TypeBinaryExpression(TypeExpression):
    left: TypeExpression
    op: str
    right: TypeExpression


@ dataclass
class TypeAngleExpression(TypeExpression):
    name: str
    expr_list: List[TypeExpression]

@ dataclass
class TypeIdExpression(TypeExpression):
    name: str

@ dataclass
class TypeTypeExpression(TypeExpression):
    type_obj: Any 

@ dataclass
class TypeDerefExpression(TypeExpression):
    expr: TypeExpression


@ dataclass
class TypePtrExpression(TypeExpression):
    expr: TypeExpression


@ dataclass
class TypeIndexExpression(TypeExpression):
    expr: TypeExpression
    name: str


# misc

class SemanticStatus(Enum):
    TYPE_EXPR = 1
    VALUE_EXPR = 2


class SemanticEnvironment:
    def __init__(self):
        self.status_stack = []
        self.in_func = False
        self.in_struct = False

    def add(self, ss):
        self.status_stack.append(ss)

    def pop(self):
        self.status_stack.pop()

    def top(self):
        return self.status_stack[-1]


SS = SemanticStatus
SE = SemanticEnvironment


# visitor methods


@add_method_parse_semantics(pr.CompilationUnit)
def _(self: pr.CompilationUnit, se: SemanticEnvironment):
    return Program(
        [d.parse_semantics(se) for d in self.definitionList.flist],
        [d.parse_semantics(se) for d in self.definitionList.slist]
    )


@add_method_parse_semantics(pr.StructDefinition)
def _(self: pr.StructDefinition, se: SE):
    se.in_struct = True
    sl = self.block.parse_semantics(se)
    se.in_struct = False
    if hasattr(self.expr.expr, "id"):
        return StructDefinition(
            name=self.expr.expr.id,
            type_parameter_names=[],
            statement_list = sl
        )
    else:
        return StructDefinition(
            name=self.expr.expr.expr.expr.expr.id,
            type_parameter_names=[
                i.expr.id for i in self.expr.expr.expr.expr_list],
            statement_list = sl
        )


@add_method_parse_semantics(pr.FunctionDefinition)
def _(self: pr.FunctionDefinition, se: SE):
    se.in_func = True
    sl = self.block.parse_semantics(se)
    se.in_func = False

    se.add(SS.TYPE_EXPR)
    if self.expr_ret is not None:
        expr_ret = self.expr_ret.parse_semantics(se)
    else:
        expr_ret = TypeAngleExpression("void", [])
    se.pop()
    pce = self.expr.expr.expr
    if hasattr(pce.expr.expr, "id"):
        name = pce.expr.expr.id
        type_parameter_names = []
        parameters = [e.expr.id for e in pce.expr_list]
    else:
        name = pce.expr.expr.expr.expr.expr.id
        type_parameter_names = [
            e.expr.id for e in pce.expr.expr.expr.expr_list]
        parameters = [e.expr.id for e in pce.expr_list]
    res = FunctionDefinition(name, type_parameter_names,
                             parameters, expr_ret, sl)
    return res


@add_method_parse_semantics(pr.Block)
def _(self: pr.Block, se: SE):
    temp = [s.parse_semantics(se) for s in self.statementList]
    return [t for t in temp if t is not None]


@add_method_parse_semantics(pr.Statement)
def _(self: pr.Statement, se: SE):
    return self.statement.parse_semantics(se)


@add_method_parse_semantics(pr.ExpressionStatement)
def _(self, se: SE):
    if not se.in_func:
        raise RuntimeError("Cant parse expression out of func!")
    se.add(SS.VALUE_EXPR)
    a = self.expr.parse_semantics(se)
    se.pop()
    return ExpressionStatement(a)


@add_method_parse_semantics(pr.DeclarationStatement)
def _(self, se: SE):
    if se.top() != SS.STRUCT:
        raise RuntimeError("Cant declare memeber out of struct!")
    name = self.expr2.expr.id
    se.add(SS.TYPE_EXPR)
    a = self.expr1.parse_semantics(se)
    se.pop()
    return MemberDeclarationStatement(name, a)


@add_method_parse_semantics(pr.TypeStatement)
def _(self, se: SE):
    name = self.left.expr.id
    se.add(SS.TYPE_EXPR)
    a = self.right.parse_semantics(se)
    se.pop()
    if se.in_func:
        return TypeDeclarationStatementFunction(name, a)
    else:
        return TypeDeclarationStatementStruct(name, a)



@add_method_parse_semantics(pr.BlankStatement)
def _(self, se: SE):
    print(self.name)
    return None


@add_method_parse_semantics(pr.BlockStatement)
def _(self, se: SE):
    if se.in_func:
        raise RuntimeError("Cant declare new block out of func!")
    a = self.block.parse_semantics(se)
    return BlockStatement(a)


@add_method_parse_semantics(pr.InitStatement)
def _(self, se: SE):
    if not se.in_func:
        name = self.name.expr.id
        se.add(SS.TYPE_EXPR)
        a = self.expr.parse_semantics(se)
        se.pop()
        return MemberDeclarationStatement(name, a)
    else:
        name = self.name.expr.id
        se.add(SS.VALUE_EXPR)
        a = self.expr.parse_semantics(se)
        se.pop()
        return InitStatement(name, a)


@add_method_parse_semantics(pr.AssignmentStatement)
def _(self, se: SE):
    if not se.in_func:
        raise RuntimeError("Cant assign to a var out of func!")
    se.add(SS.VALUE_EXPR)
    l = self.left.parse_semantics(se)
    r = self.right.parse_semantics(se)
    se.pop()
    return AssignmentStatement(l, r)


@add_method_parse_semantics(pr.IfElseStatement)
def _(self, se: SE):
    if not se.in_func:
        raise RuntimeError("Cant use if/else out of func!")
    se.add(SS.VALUE_EXPR)
    a = self.expr.parse_semantics(se)
    if self.blockElse is None:
        res = IfElseStatement(
            a,
            self.blockIf.parse_semantics(se),
            Block([])
        )
    else:
        res = IfElseStatement(
            a,
            self.blockIf.parse_semantics(se),
            self.blockElse.parse_semantics(se),
        )
    se.pop()
    return res


@add_method_parse_semantics(pr.ForStatement)
def _(self, se: SE):
    if not se.in_func:
        raise RuntimeError("Cant use for out of func!")
    se.add(SS.VALUE_EXPR)
    res = ForStatement(
        self.statementInit.parse_semantics(se),
        self.exprCheck.parse_semantics(se),
        self.statementChange.parse_semantics(se),
        self.block.parse_semantics(se)
    )
    se.pop()
    return res


@add_method_parse_semantics(pr.WhileStatement)
def _(self: pr.WhileStatement, se: SE):
    if not se.in_func:
        raise RuntimeError("Cant use while out of func!")
    se.add(SS.VALUE_EXPR)
    res = WhileStatement(
        self.exprCheck.parse_semantics(se),
        self.block.parse_semantics(se)
    )
    se.pop()
    return res


@add_method_parse_semantics(pr.ReturnStatement)
def _(self: pr.ReturnStatement, se: SE):
    if not se.in_func:
        raise RuntimeError("Cant use return out of func!")
    if self.expr is None:
        return ReturnStatement(None)
    else:
        se.add(SS.VALUE_EXPR)
        e = self.expr.parse_semantics(se)
        se.pop()
        return ReturnStatement(e)


@add_method_parse_semantics(pr.BreakStatement)
def _(self: pr.BreakStatement, se: SE):
    if not se.in_func:
        raise RuntimeError("Cant use break out of func!")


@add_method_parse_semantics(pr.Expression)
def _(self: pr.Expression, se: SE):
    return self.expr.parse_semantics(se)


@add_method_parse_semantics(pr.IdExpression)
def _(self: pr.IdExpression, se: SE):
    if se.top() == SS.TYPE_EXPR:
        return TypeIdExpression(self.id)
    else:
        return IdExpression(self.id)


@add_method_parse_semantics(pr.BinaryExpression)
def _(self: pr.BinaryExpression, se: SE):
    if se.top() == SS.TYPE_EXPR:
        return TypeBinaryExpression(
            self.left.parse_semantics(se),
            ops_mapping[self.op],
            self.right.parse_semantics(se)
        )
    if se.top() == SS.VALUE_EXPR:
        return BinaryExpression(
            self.left.parse_semantics(se),
            ops_mapping[self.op],
            self.right.parse_semantics(se)
        )
    raise RuntimeError("Shouldn't have gotten here!")


@add_method_parse_semantics(pr.UnaryExpression)
def _(self: pr.UnaryExpression, se: SE):
    return self.expr.parse_semantics(se)


@add_method_parse_semantics(pr.ParenthesesExpression)
def _(self: pr.ParenthesesExpression, se: SE):
    return self.expr.parse_semantics(se)


@add_method_parse_semantics(pr.AngleCallExpression)
def _(self: pr.AngleCallExpression, se: SE):
    if se.top() != SS.TYPE_EXPR:
        raise RuntimeError("Angle call is a part of type expression!")
    return TypeAngleExpression(
        self.expr.parse_semantics(se).name,
        [s.parse_semantics(se) for s in self.expr_list]
    )


@add_method_parse_semantics(pr.ParenthesesCallExpression)
def _(self: pr.ParenthesesCallExpression, se: SE):
    if se.top() != SS.VALUE_EXPR:
        raise RuntimeError("Parentheses call is\
                a part of value expression!")
    if hasattr(self.expr.expr, "id"):
        name = self.expr.expr.id
        type_expr = []
        se.add(SS.VALUE_EXPR)
        args = [e.parse_semantics(se) for e in self.expr_list]
        se.pop()
    else:
        name = self.expr.expr.expr.expr.expr.id
        se.add(SS.TYPE_EXPR)
        type_expr = [e.parse_semantics(se) for
                     e in self.expr.expr.expr.expr_list]
        se.pop()
        se.add(SS.VALUE_EXPR)
        args = [e.parse_semantics(se) for e in self.expr_list]
        se.pop()

    return CallExpression(name, type_expr, args)


@add_method_parse_semantics(pr.DotExpression)
def _(self: pr.DotExpression, se: SE):
    if se.top() == SS.VALUE_EXPR:
        return MemberIndexExpression(
            self.left.parse_semantics(se),
            self.right.expr.id
        )
    if se.top() == SS.TYPE_EXPR:
        return TypeIndexExpression(
            self.left.parse_semantics(se),
            self.right.expr.id
        )


@add_method_parse_semantics(pr.BracketCallExpression)
def _(self: pr.BracketCallExpression, se: SE):
    if se.top() != SS.VALUE_EXPR:
        raise RuntimeError("Bracket call not available in typeexpr")
    e1 = self.expr1.parse_semantics(se)
    e2 = self.expr1.parse_semantics(se)
    return BracketCallExpression(e1, e2)


@add_method_parse_semantics(pr.DereferenceExpression)
def _(self: pr.DereferenceExpression, se: SE):
    if se.top() == SS.VALUE_EXPR:
        e = self.expr.parse_semantics(se)
        return DerefExpression(e)
    if se.top() == SS.TYPE_EXPR:
        e = self.expr.parse_semantics(se)
        return TypeDerefExpression(e)


@add_method_parse_semantics(pr.AddressExpression)
def _(self: pr.AddressExpression, se: SE):
    if se.top() == SS.VALUE_EXPR:
        e = self.expr.parse_semantics(se)
        return AddressExpression(e)
    if se.top() == SS.TYPE_EXPR:
        e = self.expr.parse_semantics(se)
        return TypePtrExpression(e)


@add_method_parse_semantics(pr.LiteralExpression)
def _(self: pr.LiteralExpression, se: SE):
    if se.top() != SS.VALUE_EXPR:
        raise RuntimeError("literals can only be runtime")
    return self.value.parse_semantics(se)


@add_method_parse_semantics(pr.IntLiteral)
def _(self: pr.IntLiteral, se: SE):
    return IntLiteralExpression(self.value, self.size)


@add_method_parse_semantics(pr.BoolLiteral)
def _(self: pr.BoolLiteral, se: SE):
    return BoolLiteralExpression(self.value)

# ARTIFICIAL STATEMENTS
@dataclass
class MemoryCopyStatement(FunctionStatement):
    dest: str
    src: str

@dataclass
class HeapAllocStatement(FunctionStatement):
    dest: str
    type_expr: TypeExpression
    value_expr: ValueExpression

@dataclass
class OutStatement(FunctionStatement):
    src: str
    type_expr: TypeExpression

@dataclass
class InStatement(FunctionStatement):
    dest: str
    type_expr: TypeExpression


#



