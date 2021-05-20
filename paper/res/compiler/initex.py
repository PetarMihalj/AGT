@add_method_parse_semantics(pr.InitStatement)
def _(self, se: SE):
    if not se.in_func:
        name = self.nameexpr.expr.id
        se.add(SS.TYPE_EXPR)
        a = self.expr.parse_semantics(se)
        se.pop()
        return MemberDeclarationStatement(name, a)
    else:
        name = self.nameexpr.expr.id
        se.add(SS.VALUE_EXPR)
        a = self.expr.parse_semantics(se)
        se.pop()
        return InitStatement(name, a)
