from dataclasses import dataclass
from typing import List, Any, Tuple


class TreeNode:
    pass


@dataclass
class Program(TreeNode):
    function_definitions: List
    struct_definitions: List


@dataclass
class FunctionDefinition(TreeNode):
    name: str
    type_parameters: List[str]
    parameters: List[List[str]]
    block: Any


@dataclass
class StructDefinition(TreeNode):
    name: str
    type_parameter_names: List[str]
    block: Any


@dataclass
class Block(TreeNode):
    statement_list: List[Any]


@dataclass
class ExpressionStatement(TreeNode):
    expr: Any


@dataclass
class MemberDeclarationStatement(TreeNode):
    type_expr: Any
    name: Any


@dataclass
class BlankStatement(TreeNode):
    pass


@dataclass
class TypeDeclarationStatement(TreeNode):
    type_expr: Any
    name: Any


@dataclass
class BlockStatement(TreeNode):
    block: Any


@dataclass
class AssignmentStatement(TreeNode):
    name: Any
    expr: Any


@dataclass
class InitStatement(TreeNode):
    name: Any
    expr: Any


@dataclass
class WhileStatement(TreeNode):
    expr_check: Any
    block: Any


@dataclass
class ForStatement(TreeNode):
    stat_init: Any
    expr_check: Any
    stat_change: Any
    block: Any


@dataclass
class IfElseStatement(TreeNode):
    expr: Any
    block_true: Any
    block_false: Any


@dataclass
class ReturnStatement(TreeNode):
    expr: Any


@dataclass
class BreakStatement(TreeNode):
    no: int


# Runtime expressions


@dataclass
class BinaryExpression(TreeNode):
    left: Any
    op: str
    right: Any


@dataclass
class BracketCallExpression(TreeNode):
    expr: Any
    index: Any


@dataclass
class MemberIndexExpression(TreeNode):
    expr: Any
    member: str


@dataclass
class DerefExpression(TreeNode):
    expr: Any


@dataclass
class AddressExpression(TreeNode):
    expr: Any


@dataclass
class IntLiteralExpression(TreeNode):
    value: int
    signed: bool
    size: int


@dataclass
class FunctionCallExpression(TreeNode):
    name: int
    type_expr_list: List[Any]
    args: List[Any]


@dataclass
class BoolLiteralExpression(TreeNode):
    value: bool

# Type Expressions


@dataclass
class TypeBinaryExpression(TreeNode):
    left: Any
    op: str
    right: Any


@dataclass
class TypeAngleExpression(TreeNode):
    expr: Any
    expr_list: List[Any]


@dataclass
class TypeDerefExpression(TreeNode):
    expr: Any


@dataclass
class TypePtrExpression(TreeNode):
    expr: Any


@dataclass
class TypeMemberIndexExpression(TreeNode):
    expr: Any
    member: str
