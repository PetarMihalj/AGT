import semantic_ast as sa
import type_system as ts
from type_engine import TypingContext as TC

from helpers import add_method
from typing import List, Union
import flat_ir as ir


class SyntaxError(RuntimeError):
    pass


class NoInferencePossibleError(RuntimeError):
    pass


@ add_method(sa.Program, "te_visit")
def _(self: sa.Program, tc: TC):
    raise RuntimeError("this is not parsed directly")


@ add_method(sa.StructDefinition, "te_visit")
def _(self: sa.StructDefinition, tc: TC,
      type_args: List[ts.Type],
      ):
    if len(type_args) != len(self.type_parameter_names):
        return None
    s = ts.StructType(self.name)

    s.types = dict([
        a for a in zip(self.type_parameter_names, type_args)
    ])

    self.block.te_visit(tc, s)

    return s


@ add_method(sa.FunctionDefinition, "te_visit")
def _(self, tc: TC,
      type_args: List[ts.Type],
      args: List[ts.Type],
      ):
    if len(type_args) != len(self.type_parameter_names) or\
            len(args) != len(self.parameter_names):
        return None
    f = ts.FunctionType(self.name)

    f.parameter_names_ordered = self.parameter_names
    f.type_parameters = dict([
        a for a in zip(self.type_parameter_names, type_args)
    ])
    f.parameters = dict([
        a for a in zip(self.parameter_names, args)
    ])

    self.block.te_visit(tc, f)


@ add_method(sa.Block, "te_visit")
def _(self: sa.Block, tc: TC,
        sf: Union[ts.FunctionType, ts.StructType]):
    for s in self.statement_list:
        s.te_visit(tc, sf)


@ add_method(sa.ExpressionStatement, "te_visit")
def _(self: sa.ExpressionStatement, tc: TC,
        sf: Union[ts.FunctionType, ts.StructType]):
    self.expr.te_visit(tc, sf)


@ add_method(sa.MemberDeclarationStatement, "te_visit")
def _(self: sa.MemberDeclarationStatement, tc: TC,
        sf: Union[ts.FunctionType, ts.StructType]):
    res = self.type_expr.te_visit(tc, sf)
    sf.types[self.name] = res




@ add_method(sa.TypeDeclarationStatement, "te_visit")
def _(self: sa.TypeDeclarationStatement, tc: TC,
        sf: Union[ts.FunctionType, ts.StructType]):
    res = self.type_expr.te_visit(tc, sf)
    sf.types[self.name] = res
