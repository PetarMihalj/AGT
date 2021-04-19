import semantic_ast as sa
import type_system as ts
from type_engine import TypingContext as TC
from type_engine import LogTypes 

from helpers import add_method_te_visit
from typing import List, Union
import flat_ir as ir


from type_engine import NoInferencePossibleError, SyntError


# structural


@add_method_te_visit(sa.Program)
def _(self: sa.Program, tc: TC):
    raise SyntError("this is not parsed directly")


@add_method_te_visit(sa.FunctionDefinition)
def _(self: sa.FunctionDefinition, tc: TC,
      type_args: List[ts.Type],
      args: List[ts.Type],
      ):
    desc = (
        self.name,
        tuple(type_args),
        tuple(args)
    )
    tc.logger.go_in()
    tc.logger.log(f"Function definition at {self.linespan[0]}", 
            LogTypes.FUNCTION_DEFINITION)


    f = ts.FunctionType(self.name)
    f.mangled_name = tc.scope_man.new_func_name(self.name)

    f.parameter_names_ordered = self.parameter_names
    f.types = dict([
        a for a in zip(self.type_parameter_names, type_args)
    ] +
        [
        a for a in zip(self.parameter_names, args)
    ])

    tc.scope_man.begin_scope()
    for name in self.type_parameter_names:
        tc.scope_man.new_var_name(name)
    for name in self.parameter_names:
        tc.scope_man.new_var_name(name)
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
    tc.scope_man.end_scope()

    # remove func, since it might contradict other alternatives
    tc.function_type_container.pop(desc)
    del f.break_label_stack

    tc.logger.go_out()
    return f


@add_method_te_visit(sa.StructDefinition)
def _(self: sa.StructDefinition, tc: TC,
      type_args: List[ts.Type],
      ):
    tc.logger.go_in()
    tc.logger.log(f"Function definition at {self.linespan[0]}", 
            LogTypes.FUNCTION_DEFINITION)
    s = ts.StructType(self.name)

    s.types = dict([
        a for a in zip(self.type_parameter_names, type_args)
    ])

    for stat in self.statement_list:
        stat.te_visit(tc, s)
    s.mangled_name = tc.scope_man.new_struct_name(self.name)

    tc.logger.go_out()

    return s


# function statements

@add_method_te_visit(sa.BlockStatement)
def _(self: sa.BlockStatement, tc: TC,
        f: ts.FunctionType):
    tc.scope_man.begin_scope()
    self.expr.te_visit(tc, f)
    tc.scope_man.end_scope()


@add_method_te_visit(sa.ExpressionStatement)
def _(self: sa.ExpressionStatement, tc: TC,
        f: ts.FunctionType):
    self.expr.te_visit(tc, f, lvalue = False)


@add_method_te_visit(sa.TypeDeclarationStatementFunction)
def _(self: sa.TypeDeclarationStatementFunction, tc: TC,
        f: ts.FunctionType):

    print("resolving type decl")
    mn = tc.scope_man.new_var_name(self.name, type_name=True)
    f.types[mn] = self.type_expr.te_visit(tc, f)


@add_method_te_visit(sa.AssignmentStatement)
def _(self: sa.AssignmentStatement, tc: TC,
        f: ts.FunctionType):
    le = self.left.te_visit(tc, f, lvalue=True)
    re = self.right.te_visit(tc, f, lvalue=False)
    if f.types[le] != f.types[re]:
        raise NoInferencePossibleError("type missmatch")
    else:
        f.flat_statements.append(ir.Assignment(le, re))


@add_method_te_visit(sa.InitStatement)
def _(self: sa.InitStatement, tc: TC,
        f: ts.FunctionType):
    mn = tc.scope_man.new_var_name(self.name)
    e = self.expr.te_visit(tc, f, lvalue=False)
    f.flat_statements.append(ir.StackAllocate(mn, f.types[e]))
    f.flat_statements.append(ir.Assignment(mn, e))


@add_method_te_visit(sa.WhileStatement)
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


@add_method_te_visit(sa.ForStatement)
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


@add_method_te_visit(sa.IfElseStatement)
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
    s.te_visit(tc, f)
    f.flat_statements.append(ir.JumpToLabel(ec, ifend))
    f.flat_statements.append(ir.Label(iffalse))
    for s in self.statment_list_false:
        s.te_visit(tc, f)
    f.flat_statements.append(ir.Label(ifend))
    tc.scope_man.end_scope()


@add_method_te_visit(sa.ReturnStatement)
def _(self: sa.ReturnStatement, tc: TC,
        f: ts.FunctionType):
    ec = self.expr_check.te_visit(tc, f, lvalue=False)
    if f.types[ec] != f.types["return"]:
        raise NoInferencePossibleError("wrong return type")
    f.flat_statements.append(ir.FunctionReturn(ec))


@add_method_te_visit(sa.BreakStatement)
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


@add_method_te_visit(sa.MemberDeclarationStatement)
def _(self: sa.MemberDeclarationStatement, tc: TC,
        s: ts.StructType):
    t = self.type_expr.te_visit(tc, s)
    s.types[self.name] = t
    s.members.append(self.name)


@add_method_te_visit(sa.TypeDeclarationStatementStruct)
def _(self: sa.TypeDeclarationStatementStruct, tc: TC,
        s: ts.StructType):
    t = self.type_expr.te_visit(tc, s)
    s.types[self.name] = t


# value expressions


@add_method_te_visit(sa.BinaryExpression)
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


@add_method_te_visit(sa.BracketCallExpression)
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


@add_method_te_visit(sa.MemberIndexExpression)
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


@add_method_te_visit(sa.DerefExpression)
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


@add_method_te_visit(sa.AddressExpression)
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


@add_method_te_visit(sa.IntLiteralExpression)
def _(self: sa.IntLiteralExpression, tc: TC,
        f: ts.FunctionType, lvalue):
    if lvalue:
        raise NoInferencePossibleError("cant lvalue intliteral")
    tmp = tc.scope_man.new_tmp_var_name("int literal")
    f.types[tmp] = ts.IntType(self.size)
    f.flat_statements.append(ir.IntConstantAssignment(tmp,
                                                      self.value,
                                                      self.size))
    return tmp


@add_method_te_visit(sa.BoolLiteralExpression)
def _(self: sa.BoolLiteralExpression, tc: TC,
        f: ts.FunctionType, lvalue):
    if lvalue:
        raise NoInferencePossibleError("cant lvalue boolliteral")
    tmp = tc.scope_man.new_tmp_var_name("bool literal")
    f.types[tmp] = ts.BoolType()
    f.flat_statements.append(ir.BoolConstantAssignment(tmp,
                                                       self.value))
    return tmp


@add_method_te_visit(sa.CallExpression)
def _(self: sa.CallExpression, tc: TC,
        f: ts.FunctionType, lvalue):
    if lvalue:
        raise NoInferencePossibleError("cant lvalue call expr")
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
    except NoInferencePossibleError:
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
        except NoInferencePossibleError:
            raise NoInferencePossibleError("cant synth callexpr")


# type expressions

@add_method_te_visit(sa.TypeBinaryExpression)
def _(self: sa.TypeBinaryExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):

    le = self.left.te_visit(tc, sf)
    lr = self.right.te_visit(tc, sf)
    try:
        rt = tc.resolve_struct(self.op, [le, lr])
    except NoInferencePossibleError:
        raise NoInferencePossibleError(f"no operator {self.op}")

    return rt


@add_method_te_visit(sa.TypeAngleExpression)
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
    print(texprs)
    rt = tc.resolve_struct(self.name, texprs)

    return rt

@add_method_te_visit(sa.TypeIdExpression)
def _(self: sa.TypeIdExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):

    print(self.name)
    print(sf.types)
    if isinstance(sf, ts.StructType):
        if self.name in sf.types:
            return sf.types[self.name]
    elif isinstance(sf, ts.FunctionType):
        mn = tc.scope_man.get_var_name(self.name)
        if mn is not None:
            return sf.types[self.name]
    print("NOT")

    rt = tc.resolve_struct(self.name, [])

    return rt

@add_method_te_visit(sa.TypeDerefExpression)
def _(self: sa.TypeDerefExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):

    e = self.expr.te_visit(tc, sf)
    if e is None: return None

    if isinstance(e, ts.PointerType):
        return e.pointed
    else:
        self.logger.log(f"[ERR] Can't deref non pointer!",
                LogTypes.FUNCTION_OR_STRUCT_DEFINITION)
        return None


@add_method_te_visit(sa.TypePtrExpression)
def _(self: sa.TypePtrExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):

    e = self.expr.te_visit(tc, sf)
    if e is None: return None

    return ts.PointerType(e)


@add_method_te_visit(sa.TypeIndexExpression)
def _(self: sa.TypeIndexExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):

    e = self.expr.te_visit(tc, sf)
    if e is None: return None

    if not isinstance(e, ts.StructType):
        self.logger.log(f"[ERR] TypeIndexExpression must be on struct!",
                LogTypes.FUNCTION_OR_STRUCT_DEFINITION)
        return None
    return e.types[self.name]
