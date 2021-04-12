
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
