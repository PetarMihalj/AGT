from helpers import tree_print
from syntactic_ast import compile_syntactic_ast
from dataclasses import dataclass
from typing import List

from type_engine import TypeEngine
import type_system as ts
import parser_rules as pr
from enum import Enum
import sys


class TreeNode:
    pass


class Statement:
    pass


class Expression:
    pass


class RuntimeExpression:
    pass


class TypeExpression:
    pass


@dataclass
class Program(TreeNode):
    function_definitions: List['FunctionDefinition']
    struct_definitions: List['StructDefinition']

    def te_visit(self, te: TypeEngine):
        raise RuntimeExpression("this is not parsed directly")


@dataclass
class FunctionDefinition(TreeNode):
    name: str
    type_parameter_names: List[str]
    parameter_names: List[str]
    expr_ret: TypeExpression
    block: 'Block'

    def te_visit(self, te: TypeEngine,
                 type_args: List[ts.Type],
                 args: List[ts.Type],
                 ):
        if len(type_args) != len(self.type_parameter_names) or\
                len(args) != len(self.parameter_names):
            return None
        f = ts.FunctionType()
        f.parameter_names = self.parameter_names

        f.type_parameters = dict([
            a for a in zip(self.type_parameter_names, type_args)
        ])
        f.parameters = dict([
            a for a in zip(self.parameter_names, args)
        ])

        self.block.te_visit(te, f)


@ dataclass
class StructDefinition(TreeNode):
    name: str
    type_parameter_names: List[str]
    block: 'Block'


@ dataclass
class Block(TreeNode):
    statement_list: List['Statement']

    def te_visit(self, te: TypeEngine, fsd):
        for stat in self.statement_list:
            stat.te_visit(te, fsd)
        if isinstance(fsd, FunctionDefinition):
            f: FunctionDefinition = fsd
        elif isinstance(fsd, StructDefinition):
            s: StructDefinition = fsd


@ dataclass
class ExpressionStatement(TreeNode):
    expr: RuntimeExpression

    def te_visit(self, te: TypeEngine, f: FunctionDefinition):
        rexpr = self.expr.te_visit(te, f)
        return rexpr


@ dataclass
class MemberDeclarationStatement(TreeNode):
    type_expr: TypeExpression
    name: str

    def te_visit(self, te: TypeEngine, f: FunctionDefinition):
        rexpr = self.expr.te_visit(te, f)
        return rexpr


@ dataclass
class BlankStatement(TreeNode):
    def te_visit(self, te, fsd):
        pass


@ dataclass
class TypeDeclarationStatement(TreeNode):
    type_expr: TypeExpression
    name: str


@ dataclass
class BlockStatement(TreeNode):
    block: Block


@ dataclass
class AssignmentStatement(TreeNode):
    left: RuntimeExpression
    right: RuntimeExpression


@ dataclass
class InitStatement(TreeNode):
    name: str
    expr: RuntimeExpression


@ dataclass
class WhileStatement(TreeNode):
    expr_check: RuntimeExpression
    block: Block


@ dataclass
class ForStatement(TreeNode):
    stat_init: Statement
    expr_check: RuntimeExpression
    stat_change: Statement
    block: Block


@ dataclass
class IfElseStatement(TreeNode):
    expr: RuntimeExpression
    block_true: Block
    block_false: Block


@ dataclass
class ReturnStatement(TreeNode):
    expr: RuntimeExpression


@ dataclass
class BreakStatement(TreeNode):
    no: int


# Runtime expressions


@ dataclass
class BinaryExpression(TreeNode):
    left: RuntimeExpression
    op: str
    right: RuntimeExpression


@ dataclass
class BracketCallExpression(TreeNode):
    expr: RuntimeExpression
    index: RuntimeExpression


@ dataclass
class MemberIndexExpression(TreeNode):
    expr: RuntimeExpression
    member: RuntimeExpression


@ dataclass
class DerefExpression(TreeNode):
    expr: RuntimeExpression


@ dataclass
class AddressExpression(TreeNode):
    expr: RuntimeExpression


@ dataclass
class IntLiteralExpression(TreeNode):
    value: int
    size: int


@ dataclass
class CallExpression(TreeNode):
    name: int
    type_expr_list: List[TypeExpression]
    args: List[RuntimeExpression]


@ dataclass
class BoolLiteralExpression(TreeNode):
    value: bool

# Type Expressions


@ dataclass
class TypeBinaryExpression(TreeNode):
    left: TypeExpression
    op: str
    right: TypeExpression


@ dataclass
class TypeAngleExpression(TreeNode):
    name: str
    expr_list: List[TypeExpression]


@ dataclass
class TypeDerefExpression(TreeNode):
    expr: TypeExpression


@ dataclass
class TypePtrExpression(TreeNode):
    expr: TypeExpression


@ dataclass
class TypeMemberIndexExpression(TreeNode):
    expr: TypeExpression
    member: str


# misc

class SemanticStatus(Enum):
    UNKNOWN = 0
    FUNC = 1
    STRUCT = 2
    TYPE_EXPR = 3
    RUNTIME_EXPR = 4


class SemanticEnvironment:
    def __init__(self):
        self.status_stack = [SemanticStatus.UNKNOWN]

    def add(self, ss):
        self.status_stack.append(ss)

    def pop(self):
        self.status_stack.pop()

    def top(self):
        return self.status_stack[-1]


SS = SemanticStatus
SE = SemanticEnvironment


def add_method(cls, name):
    def go(func):
        setattr(cls, name, func)


# visitor methods

@add_method(pr.CompilationUnit, "parse_semantics")
def _(self: pr.CompilationUnit, se: SemanticEnvironment):
    return Program(
        [d.parse_semantics(se) for d in self.definitionList.flist],
        [d.parse_semantics(se) for d in self.definitionList.slist]
    )


@add_method(pr.StructDefinition, "parse_semantics")
def _(self: pr.StructDefinition, se: SE):
    se.add(SS.STRUCT)
    sl = self.block.parse_semantics(se)
    se.pop()
    if hasattr(self.expr.expr, "id"):
        return StructDefinition(
            name=self.expr.expr.id,
            type_parameter_names=[],
            block=Block(sl)
        )
    else:
        return StructDefinition(
            name=self.expr.expr.expr.expr.expr.id,
            type_parameter_names=[
                i.expr.id for i in self.expr.expr.expr.expr_list],
            block=Block(sl)
        )


@add_method(pr.FunctionDefinition, "parse_semantics")
def _(self: pr.FunctionDefinition, se: SE):
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
        parameters = [e.expr.id for e in pce.expr_list]
    else:
        name = pce.expr.expr.expr.expr.expr.id
        type_parameter_names = [
            e.expr.id for e in pce.expr.expr.expr.expr_list]
        parameters = [e.expr.id for e in pce.expr_list]
    res = FunctionDefinition(name, type_parameter_names,
                             parameters, expr_ret, Block(sl))
    return res


@add_method(pr.Block, "parse_semantics")
def _(self: pr.Block, se: SE):
    return [s.parse_semantics(se) for s in self.statementList]


@add_method(pr.Statement, "parse_semantics")
def _(self: pr.Statement, se: SE):
    return self.statement.parse_semantics(se)


@add_method(pr.ExpressionStatement, "parse_semantics")
def _(self, se: SE):
    if se.top() != SS.FUNC:
        raise RuntimeError("Cant parse expression out of func!")
    se.add(SS.RUNTIME_EXPR)
    a = self.expr.parse_semantics(se)
    se.pop()
    return a


@add_method(pr.DeclarationStatement, "parse_semantics")
def _(self, se: SE):
    if se.top() != SS.STRUCT:
        raise RuntimeError("Cant declare memeber out of struct!")
    name = self.expr2.expr.id
    se.add(SS.TYPE_EXPR)
    a = self.expr1.parse_semantics(se)
    se.pop()
    return MemberDeclarationStatement(a, name)


@add_method(pr.TypeStatement, "parse_semantics")
def _(self, se: SE):
    name = self.left.expr.id
    se.add(SS.TYPE_EXPR)
    a = self.right.parse_semantics(se)
    se.pop()
    return TypeDeclarationStatement(a, name)


@add_method(pr.BlankStatement, "parse_semantics")
def _(self, se: SE):
    return BlankStatement()


@add_method(pr.BlockStatement, "parse_semantics")
def _(self, se: SE):
    if se.top() != SS.FUNC:
        raise RuntimeError("Cant declare new block out of func!")
    a = self.block.parse_semantics(se)
    return la.BlockStatement(a)


@add_method(pr.InitStatement, "parse_semantics")
def _(self, se: SE):
    if se.top() != SS.FUNC:
        name = self.name.expr.id
        se.add(SS.TYPE_EXPR)
        a = self.expr.parse_semantics(se)
        se.pop()
        return MemberDeclarationStatement(name, a)
    else:
        name = self.name.expr.id
        se.add(SS.RUNTIME_EXPR)
        a = self.expr.parse_semantics(se)
        se.pop()
        return InitStatement(name, a)


@add_method(pr.FunctionDefinition, "parse_semantics")
def _(self, se: SE):
    if se.top() != SS.FUNC:
        raise RuntimeError("Cant assign to a var out of func!")
    se.add(SS.RUNTIME_EXPR)
    l = self.left.parse_semantics(se)
    r = self.right.parse_semantics(se)
    se.pop()
    return AssignmentStatement(l, r)


@add_method(pr.FunctionDefinition, "parse_semantics")
def _(self, se: SE):
    if se.top() != SS.FUNC:
        raise RuntimeError("Cant use if/else out of func!")
    se.add(SS.RUNTIME_EXPR)
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


@add_method(pr.ForStatement, "parse_semantics")
def _(self, se: SE):
    if se.top() != SS.FUNC:
        raise RuntimeError("Cant use for out of func!")
    se.add(SS.RUNTIME_EXPR)
    res = ForStatement(
        self.statementInit.parse_semantics(se),
        self.exprCheck.parse_semantics(se),
        self.statementChange.parse_semantics(se),
        self.block.parse_semantics(se)
    )
    se.pop()
    return res


@add_method(pr.WhileStatement, "parse_semantics")
def _(self: pr.WhileStatement, se: SE):
    if se.top() != SS.FUNC:
        raise RuntimeError("Cant use while out of func!")
    se.add(SS.RUNTIME_EXPR)
    res = WhileStatement(
        self.exprCheck.parse_semantics(se),
        self.block.parse_semantics(se)
    )
    se.pop()
    return res


@add_method(pr.ReturnStatement, "parse_semantics")
def _(self: pr.ReturnStatement, se: SE):
    if se.top() != SS.FUNC:
        raise RuntimeError("Cant use return out of func!")
    if self.expr is None:
        return ReturnStatement(None)
    else:
        se.add(SS.RUNTIME_EXPR)
        e = self.expr.parse_semantics(se)
        se.pop()
        return ReturnStatement(e)


@add_method(pr.BreakStatement, "parse_semantics")
def _(self: pr.BreakStatement, se: SE):
    if se.top() != SS.FUNC:
        raise RuntimeError("Cant use break out of func!")


@add_method(pr.Expression, "parse_semantics")
def _(self: pr.Expression, se: SE):
    return self.expr.parse_semantics(se)


@add_method(pr.IdExpression, "parse_semantics")
def _(self: pr.IdExpression, se: SE):
    return self.id


@add_method(pr.BinaryExpression, "parse_semantics")
def _(self: pr.BinaryExpression, se: SE):
    if se.top() == SS.TYPE_EXPR:
        return TypeBinaryExpression(
            self.left.parse_semantics(se),
            self.op,
            self.right.parse_semantics(se)
        )
    if se.top() == SS.RUNTIME_EXPR:
        return BinaryExpression(
            self.left.parse_semantics(se),
            self.op,
            self.right.parse_semantics(se)
        )
    raise RuntimeError("Shouldn't have gotten here!")


@add_method(pr.UnaryExpression, "parse_semantics")
def _(self: pr.UnaryExpression, se: SE):
    return self.expr.parse_semantics(se)


@add_method(pr.ParenthesesExpression, "parse_semantics")
def _(self: pr.ParenthesesExpression, se: SE):
    return self.expr.parse_semantics(se)


@add_method(pr.AngleCallExpression, "parse_semantics")
def _(self: pr.AngleCallExpression, se: SE):
    if se.top() != SS.TYPE_EXPR:
        raise RuntimeError("Angle call is a part of type expression!")
    return TypeAngleExpression(
        self.expr.parse_semantics(se),
        [s.parse_semantics(se) for s in self.expr_list]
    )


@add_method(pr.ParenthesesCallExpression, "parse_semantics")
def _(self: pr.ParenthesesCallExpression, se: SE):
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

    return CallExpression(name, type_expr, args)


@add_method(pr.DotExpression, "parse_semantics")
def _(self: pr.DotExpression, se: SE):
    if se.top() == SS.RUNTIME_EXPR:
        return MemberIndexExpression(
            self.left.parse_semantics(se),
            self.right.expr.id
        )
    if se.top() == SS.TYPE_EXPR:
        return TypeMemberIndexExpression(
            self.left.parse_semantics(se),
            self.right.expr.id
        )


@add_method(pr.BracketCallExpression, "parse_semantics")
def _(self: pr.BracketCallExpression, se: SE):
    if se.top() != SS.RUNTIME_EXPR:
        raise RuntimeError("Bracket call not available in typeexpr")
    e1 = self.expr1.parse_semantics(se)
    e2 = self.expr1.parse_semantics(se)
    return BracketCallExpression(e1, e2)


@add_method(pr.DereferenceExpression, "parse_semantics")
def _(self: pr.DereferenceExpression, se: SE):
    if se.top() == SS.RUNTIME_EXPR:
        e = self.expr.parse_semantics(se)
        return DerefExpression(e)
    if se.top() == SS.TYPE_EXPR:
        e = self.expr.parse_semantics(se)
        return TypeDerefExpression(e)


@add_method(pr.AddressExpression, "parse_semantics")
def _(self: pr.AddressExpression, se: SE):
    if se.top() == SS.RUNTIME_EXPR:
        e = self.expr.parse_semantics(se)
        return AddressExpression(e)
    if se.top() == SS.TYPE_EXPR:
        e = self.expr.parse_semantics(se)
        return TypePtrExpression(e)


@add_method(pr.LiteralExpression, "parse_semantics")
def _(self: pr.LiteralExpression, se: SE):
    if se.top() != SS.RUNTIME_EXPR:
        raise RuntimeError("literals can only be runtime")
    return self.value.parse_semantics(se)


@add_method(pr.IntLiteral, "parse_semantics")
def _(self: pr.IntLiteral, se: SE):
    return IntLiteralExpression(self.value, self.size)


@add_method(pr.BoolLiteral, "parse_semantics")
def _(self: pr.BoolLiteral, se: SE):
    return BoolLiteralExpression(self.value)
# misc


def compile_semantic_ast(syntactic_ast):
    se = SemanticEnvironment()
    return syntactic_ast.parse_semantics(se)


if __name__ == '__main__':
    data = open(sys.argv[1]).read()
    syn_ast = compile_syntactic_ast(data)
    tree_print(syn_ast)
    print('\n'*3)

    sem_ast = compile_semantic_ast(syn_ast)
    tree_print(sem_ast)
    print('\n'*3)
