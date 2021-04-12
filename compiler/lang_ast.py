from dataclasses import dataclass
from typing import List, Any, Tuple

from type_engine import TypeEngine
import type_system as ts


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
    type_parameters: List[str]
    parameters: List[List[str]]
    expr_ret: TypeExpression
    block: 'Block'

    def te_visit(self, te: TypeEngine):
        f = ts.FunctionType()



@dataclass
class StructDefinition(TreeNode):
    name: str
    type_parameter_names: List[str]
    block: 'Block'


@dataclass
class Block(TreeNode):
    statement_list: List['Statement']


@dataclass
class ExpressionStatement(TreeNode):
    expr: RuntimeExpression


@dataclass
class MemberDeclarationStatement(TreeNode):
    type_expr: TypeExpression
    name: str


@dataclass
class BlankStatement(TreeNode):
    pass


@dataclass
class TypeDeclarationStatement(TreeNode):
    type_expr: TypeExpression
    name: str


@dataclass
class BlockStatement(TreeNode):
    block: Block


@dataclass
class AssignmentStatement(TreeNode):
    left: RuntimeExpression
    right: RuntimeExpression


@dataclass
class InitStatement(TreeNode):
    name: str
    expr: RuntimeExpression


@dataclass
class WhileStatement(TreeNode):
    expr_check: RuntimeExpression
    block: Block


@dataclass
class ForStatement(TreeNode):
    stat_init: Statement
    expr_check: RuntimeExpression
    stat_change: Statement
    block: Block


@dataclass
class IfElseStatement(TreeNode):
    expr: RuntimeExpression
    block_true: Block
    block_false: Block


@dataclass
class ReturnStatement(TreeNode):
    expr: RuntimeExpression


@dataclass
class BreakStatement(TreeNode):
    no: int


# Runtime expressions


@dataclass
class BinaryExpression(TreeNode):
    left: RuntimeExpression
    op: str
    right: RuntimeExpression


@dataclass
class BracketCallExpression(TreeNode):
    expr: RuntimeExpression
    index: RuntimeExpression


@dataclass
class MemberIndexExpression(TreeNode):
    expr: RuntimeExpression
    member: RuntimeExpression


@dataclass
class DerefExpression(TreeNode):
    expr: RuntimeExpression


@dataclass
class AddressExpression(TreeNode):
    expr: RuntimeExpression


@dataclass
class IntLiteralExpression(TreeNode):
    value: int
    size: int


@dataclass
class CallExpression(TreeNode):
    name: int
    type_expr_list: List[TypeExpression]
    args: List[RuntimeExpression]


@dataclass
class BoolLiteralExpression(TreeNode):
    value: bool

# Type Expressions


@dataclass
class TypeBinaryExpression(TreeNode):
    left: TypeExpression
    op: str
    right: TypeExpression


@dataclass
class TypeAngleExpression(TreeNode):
    name: str
    expr_list: List[TypeExpression]


@dataclass
class TypeDerefExpression(TreeNode):
    expr: TypeExpression


@dataclass
class TypePtrExpression(TreeNode):
    expr: TypeExpression


@dataclass
class TypeMemberIndexExpression(TreeNode):
    expr: TypeExpression
    member: str
