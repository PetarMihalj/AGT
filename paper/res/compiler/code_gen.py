@add_method_te_visit(sa.MemberExpression)
def _(self: sa.MemberExpression, tc: TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, fc)
    self.lvalue = self.expr.lvalue

    if not isinstance(fc.types[e], ts.StructType):
        raise ierr.RuntimeExpressionError()

    if self.member not in fc.types[e].members:
        raise ierr.RuntimeExpressionError()

    if not self.expr.lvalue:
        put_dest(self, fc, tc, e)

    return ir.get_member(e, self.member, fc)

