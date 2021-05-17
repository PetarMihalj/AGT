@ dataclass
class InitStatement(FunctionStatement):
    name: str
    expr: ValueExpression

@ dataclass
class MemberDeclarationStatement(StructStatement):
    name: str
    type_expr: TypeExpression
