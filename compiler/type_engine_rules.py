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


# structural


@ add_method(sa.Program, "te_visit")
def _(self: sa.Program, tc: TC):
    raise RuntimeError("this is not parsed directly")


@ add_method(sa.FunctionDefinition, "te_visit")
def _(self: sa.FunctionDefinition, tc: TC,
      type_args: List[ts.Type],
      args: List[ts.Type],
      ):
    desc = (
        self.name,
        type_args,
        args
    )
    if len(type_args) != len(self.type_parameter_names) or\
            len(args) != len(self.parameter_names):
        return None
    f = ts.FunctionType(self.name)
    f.mangled_name = tc.scope_man.new_func_name(self.name)

    f.parameter_names_ordered = self.parameter_names
    f.types = dict([
        a for a in zip(self.type_parameter_names, type_args)
    ] +
        [
        a for a in zip(self.parameter_names, args)
    ])

    ret_done = False
    for s in self.statement_list:
        if not ret_done and not\
                isinstance(s, sa.TypeDeclarationStatementFunction):
            f.types["return"] = self.expr_ret.te_visit(tc, f)
            ret_done = True
            # for recursive calls, statements are not needed
            tc.function_type_container[desc] = f
        s.te_visit(tc, f)

    if not ret_done:
        f.types["return"] = self.expr_ret.te_visit(tc, f)
        ret_done = True
        # for recursive calls, statements are not needed
        tc.function_type_container[desc] = f

    # remove func, since it might contradict other alternatives
    tc.function_type_container.pop(desc)
    return f


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
    s.mangled_name = tc.scope_man.new_struct_name(self.name)

    return s


# function statements

@ add_method(sa.BlockStatement, "te_visit")
def _(self: sa.BlockStatement, tc: TC,
        f: ts.FunctionType):
    tc.scope_man.begin_scope()
    self.expr.te_visit(tc, f)
    tc.scope_man.end_scope()


@ add_method(sa.ExpressionStatement, "te_visit")
def _(self: sa.ExpressionStatement, tc: TC,
        f: ts.FunctionType):
    self.expr.te_visit(tc, f)


@ add_method(sa.TypeDeclarationStatementFunction, "te_visit")
def _(self: sa.TypeDeclarationStatementFunction, tc: TC,
        f: ts.FunctionType):

    mn = tc.scope_man.new_var_name(self.name, type_name=True)
    f.types[mn] = self.expr_ret.te_visit(tc, f)


@ add_method(sa.AssignmentStatement, "te_visit")
def _(self: sa.AssignmentStatement, tc: TC,
        f: ts.FunctionType):
    le = self.left.te_visit(tc, f, lvalue=True)
    re = self.right.te_visit(tc, f, lvalue=False)
    if f.types[le] != f.types[re]:
        raise NoInferencePossibleError("type missmatch")
    else:
        f.flat_statements.append(ir.Assignment(le, re))


@ add_method(sa.InitStatement, "te_visit")
def _(self: sa.InitStatement, tc: TC,
        f: ts.FunctionType):
    mn = tc.scope_man.new_var_name(self.name)
    e = self.expr.te_visit(tc, f, lvalue=False)
    f.flat_statements.append(ir.StackAllocate(mn, f.types[e]))
    f.flat_statements.append(ir.Assignment(mn, e))


@ add_method(sa.WhileStatement, "te_visit")
def _(self: sa.WhileStatement, tc: TC,
        f: ts.FunctionType):
    lwc = tc.scope_man.new_label_name("while check")
    lwe = tc.scope_man.new_label_name("while end")
    f.break_label_stack.append(lwe)

    tc.scope_man.begin_scope()
    ec = self.expr_check.te_visit(tc, f, lvalue=False)
    if f.types[ec] != ts.BoolType():
        raise NoInferencePossibleError("check expr must be bool")
    f.flat_statements.append(ir.Label(lwc))
    f.flat_statements.append(ir.JumpToLabelFalse(ec, lwe))
    for s in self.statement_list:
        s.te_visit(tc, f)
    f.flat_statements.append(ir.Label(lwe))
    tc.scope_man.end_scope()

    f.break_label_stack.pop()


@ add_method(sa.ForStatement, "te_visit")
def _(self: sa.ForStatement, tc: TC,
        f: ts.FunctionType):
    lfcheck = tc.scope_man.new_label_name("for check")
    lfchange = tc.scope_man.new_label_name("for change")
    lfe = tc.scope_man.new_label_name("for end")
    f.break_label_stack.append(lfe)

    tc.scope_man.begin_scope()
    self.stat_init.te_visit(tc, f)
    f.flat_statements.append(ir.Label(lfcheck))
    ec = self.expr_check.te_visit(tc, f, lvalue=False)
    if f.types[ec] != ts.BoolType():
        raise NoInferencePossibleError("check expr must be bool")
    f.flat_statements.append(ir.JumpToLabelFalse(ec, lfe))
    for s in self.statement_list:
        s.te_visit(tc, f)
    f.flat_statements.append(ir.Label(lfchange))
    self.stat_change.te_visit(tc, f)
    f.flat_statements.append(ir.JumpToLabel(lfcheck))
    tc.scope_man.end_scope()

    f.break_label_stack.pop()


@ add_method(sa.IfElseStatement, "te_visit")
def _(self: sa.IfElseStatement, tc: TC,
        f: ts.FunctionType):
    iftrue = tc.scope_man.new_label_name("if true")
    iffalse = tc.scope_man.new_label_name("if false")
    ifend = tc.scope_man.new_label_name("if end")

    tc.scope_man.begin_scope()
    ec = self.expr_check.te_visit(tc, f, lvalue=False)
    if f.types[ec] != ts.BoolType():
        raise NoInferencePossibleError("check expr must be bool")
    f.flat_statements.append(ir.JumpToLabelFalse(ec, iffalse))
    f.flat_statements.append(ir.Label(iftrue))
    for s in self.statment_list_true:
        s.te_visit(tc, f)
    f.flat_statements.append(ir.JumpToLabel(ec, ifend))
    f.flat_statements.append(ir.Label(iffalse))
    for s in self.statment_list_false:
        s.te_visit(tc, f)
    f.flat_statements.append(ir.Label(ifend))
    tc.scope_man.end_scope()


@ add_method(sa.ReturnStatement, "te_visit")
def _(self: sa.ReturnStatement, tc: TC,
        f: ts.FunctionType):
    ec = self.expr_check.te_visit(tc, f, lvalue=False)
    if f.types[ec] != f.types["return"]:
        raise NoInferencePossibleError("wrong return type")
    f.flat_statements.append(ir.FunctionReturn(ec))


@ add_method(sa.BreakStatement, "te_visit")
def _(self: sa.BreakStatement, tc: TC,
        f: ts.FunctionType):
    if self.no <= 0:
        raise NoInferencePossibleError("break must be >0")
    if self.no > len(f.break_label_stack):
        raise NoInferencePossibleError("dont have enough \
                loops to break out of")

    f.flat_statements.append(ir.JumpToLabel(
        f.break_label_stack[len(f.break_label_stack)-self.no]
    ))


# struct statements


@ add_method(sa.MemberDeclarationStatement, "te_visit")
def _(self: sa.MemberDeclarationStatement, tc: TC,
        s: ts.StructType):
    t = self.type_expr.te_visit(tc, s)
    s.types[self.name] = t
    s.members.append(self.name)


@ add_method(sa.TypeDeclarationStatementStruct, "te_visit")
def _(self: sa.TypeDeclarationStatementStruct, tc: TC,
        s: ts.StructType):
    t = self.type_expr.te_visit(tc, s)
    s.types[self.name] = t


# value expressions


@ add_method(sa.BinaryExpression, "te_visit")
def _(self: sa.BinaryExpression, tc: TC,
        f: ts.FunctionType, lvalue):
    if lvalue:
        raise NoInferencePossibleError("cant ret a lvalue")
    le = self.left.te_visit(tc, f)
    lr = self.right.te_visit(tc, f)
    tmp = tc.scope_man.new_tmp_var_name(f"{self.op}")

    opf = tc.resolve_function(self.op, [], [f.types[le], f.types[lr]])

    f.flat_statements.append(ir.FunctionCall(
        tmp, opf.mangled_name))
    f.types[tmp] = opf.types["return"]
    return opf


@ add_method(sa.BracketCallExpression, "te_visit")
def _(self: sa.BracketCallExpression, tc: TC,
        f: ts.FunctionType, lvalue):
    e = self.expr.te_visit(tc, f, lvalue=True)
    ind = self.index.te_visit(tc, f, lvalue=False)
    if not isinstance(f.types[ind], ts.IntType):
        raise NoInferencePossibleError("cant bracket with non-int index")

    tmp = tc.scope_man.new_tmp_var_name("bracket call")
    f.types[tmp] = f.types[e]

    f.flat_statements.append(ir.GetPointerOffset(tmp, e, ind))
    if lvalue:
        return tmp
    else:
        tmp2 = tc.scope_man.new_tmp_var_name("bracket call deref")
        f.types[tmp2] = f.types[e]
        f.flat_statements.append(ir.LoadValueFromPointer(tmp2, tmp))
        return tmp2


@ add_method(sa.MemberIndexExpression, "te_visit")
def _(self: sa.MemberIndexExpression, tc: TC,
        f: ts.FunctionType, lvalue):
    e = self.expr.te_visit(tc, f, lvalue=True)
    if not isinstance(f.types[e], ts.StructType):
        raise NoInferencePossibleError("cant \
                refer to a member of a non struct type")
    tmp = tc.scope_man.new_tmp_var_name("member index")
    if self.member not in f.types[e].members:
        raise NoInferencePossibleError("cant \
                refer to a nonexistant member")

    f.types[tmp] = f.types[e].types[self.member]
    f.flat_statements.append(ir.GetElementPtr(tmp, e, self.member))
    if lvalue:
        return tmp
    else:
        tmp2 = tc.scope_man.new_tmp_var_name("member index deref")
        f.types[tmp2] = f.types[e].types[self.member]
        f.flat_statements.append(ir.LoadValueFromPointer(tmp2, tmp))
        return tmp2


@ add_method(sa.DerefExpression, "te_visit")
def _(self: sa.DerefExpression, tc: TC,
        f: ts.FunctionType, lvalue):
    e = self.expr.te_visit(tc, f, lvalue=lvalue)
    if not isinstance(f.types[e], ts.PointerType):
        raise NoInferencePossibleError("cant \
                deref non pointer type")
    tmp = tc.scope_man.new_tmp_var_name("ptr deref")
    f.types[tmp] = f.types[e].pointed
    f.flat_statements.append(ir.LoadValueFromPointer(tmp, e))
    return tmp


@ add_method(sa.AddressExpression, "te_visit")
def _(self: sa.BinaryExpression, tc: TC,
        f: ts.FunctionType, lvalue):
    if lvalue:
        raise NoInferencePossibleError("cant \
                return an address which is lvalue")
    e = self.expr.te_visit(tc, f, lvalue=True)
    tmp = tc.scope_man.new_tmp_var_name("addr of")
    f.types[tmp] = ts.PointerType(f.types[e])
    f.flat_statements.append(ir.Assignment(tmp, e))
    return tmp


@ add_method(sa.IntLiteralExpression, "te_visit")
def _(self: sa.IntLiteralExpression, tc: TC,
        f: ts.FunctionType):
    tmp = tc.scope_man.new_tmp_var_name("int literal")
    f.types[tmp] = ts.IntType(self.size)
    f.flat_statements.append(ir.IntConstantAssignment(tmp,
                                                      self.value,
                                                      self.size))
    return tmp


@ add_method(sa.BoolLiteralExpression, "te_visit")
def _(self: sa.BoolLiteralExpression, tc: TC,
        f: ts.FunctionType):
    tmp = tc.scope_man.new_tmp_var_name("bool literal")
    f.types[tmp] = ts.BoolType()
    f.flat_statements.append(ir.BoolConstantAssignment(tmp,
                                                       self.value))
    return tmp


@ add_method(sa.CallExpression, "te_visit")
def _(self: sa.CallExpression, tc: TC,
        f: ts.FunctionType):
    tmp = tc.scope_man.new_tmp_var_name("bool literal")
    type_args_types = [t.te_visit(tc, f) for t in self.type_expr_list]
    args = [v.te_visit(tc, f, lvalue=False) for v in self.args]
    args_types = [f.types[a] for a in args]
    try:
        ft = tc.resolve_function(self.name, type_args_types, args_types)
        f.flat_statements.append(ir.FunctionCall(tmp,
                                                 ft.mangled_name,
                                                 args))
        f.types[tmp] = ft.types["return"]
    except ...:
        try:
            st = tc.resolve_struct(self.name, type_args_types)
            f.types[tmp] = st

            ft = tc.resolve_function(
                "__init__", [ts.PointerType(st)]+args_types)
            vd = tc.scope_man.new_tmp_var_name("void dummy")
            f.flat_statements.append(ir.FunctionCall(vd,
                                                     ft.mangled_name,
                                                     [tmp]+args))
            f.types[vd] = ft.types["return"]
        except ...:
            raise NoInferencePossibleError("cant synth callexpr")


# type expressions

@ add_method(sa.TypeBinaryExpression, "te_visit")
def _(self: sa.TypeBinaryExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):

    le = self.left.te_visit(tc, sf)
    lr = self.right.te_visit(tc, sf)
    try:
        rt = tc.resolve_struct(self.op, le, lr)
    except ...:
        raise NoInferencePossibleError(f"no operator {self.op}")

    return rt


@ add_method(sa.TypeAngleExpression, "te_visit")
def _(self: sa.TypeAngleExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):

    if len(self.expr_list) == 0:
        if isinstance(sf, ts.StructType):
            if self.name in sf.types:
                return sf.types[self.name]
        elif isinstance(sf, ts.FunctionType):
            mn = tc.scope_man.get_var_name(self.name)
            if mn is not None:
                return sf.types[self.name]

    texprs = [te.te_visit(tc, sf) for te in self.expr_list]
    try:
        rt = tc.resolve_struct(self.name, texprs)
    except ...:
        raise NoInferencePossibleError(f"no operator {self.op}")

    return rt


@ add_method(sa.TypeDerefExpression, "te_visit")
def _(self: sa.TypeDerefExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):
    e = self.expr.te_visit(tc, sf)
    if isinstance(e, ts.PointerType):
        return e.pointed
    else:
        raise NoInferencePossibleError("Cant deref non pointer")


@ add_method(sa.TypePtrExpression, "te_visit")
def _(self: sa.TypePtrExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):
    e = self.expr.te_visit(tc, sf)
    return ts.PointerType(e)


@ add_method(sa.TypeIndexExpression, "te_visit")
def _(self: sa.TypeIndexExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):
    e = self.expr.te_visit(tc, s)
    if not isinstance(e, ts.StructType):
        raise NoInferencePossibleError("Cant index non struct member type")
    return e.types[self.name]
