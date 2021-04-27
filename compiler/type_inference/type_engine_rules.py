from typing import List, Union, Any

from . import flat_ir as ir
from ..helpers import add_method_te_visit
from ..semantics_parsing import semantic_ast as sa

from .type_engine import TypingContext as TC
from .type_engine import LogTypes 

from . import type_system as ts


# structural


@add_method_te_visit(sa.Program)
def _(self: sa.Program, tc: TC):
    raise RuntimeError("this is not parsed directly")


@add_method_te_visit(sa.FunctionDefinition)
def _(self: sa.FunctionDefinition, tc: TC,
      type_args: List[ts.Type],
      args: List[ts.Type],
      ) -> Any:
    desc = (
        self.name,
        tuple(type_args),
        tuple(args)
    )
    tc.logger.go_in()
    tc.logger.log(f"Function definition at {self.linespan[0]}", 
            LogTypes.FUNCTION_DEFINITION)

    def cleanup():
        tc.scope_man.end_scope()
        if desc in tc.function_type_container:
            tc.function_type_container.pop(desc)
        del f.break_label_stack
        tc.logger.go_out()


    f = ts.FunctionType(self.name)
    f.mangled_name = tc.scope_man.new_func_name(self.name)
    f.types = {}
    f.parameter_names_ordered = []

    tc.scope_man.begin_scope()
    for name, t in zip(self.type_parameter_names, type_args):
        n = tc.scope_man.new_var_name(name)
        f.types[n] = t

    for name, t in zip(self.parameter_names, args):
        n = tc.scope_man.new_var_name(name)
        f.types[n] = t
        f.parameter_names_ordered.append(n)

    ret_done = False
    for s in self.statement_list:
        if not ret_done and not\
                isinstance(s, sa.TypeDeclarationStatementFunction):
            f.types["return"] = self.expr_ret.te_visit(tc, f)
            if f.types["return"] is None:
                tc.logger.log("Cant infer return type!", 
                        LogTypes.FUNCTION_RESOLUTION)
                cleanup()
                return None

            ret_done = True
            # for recursive calls, statements are not needed
            tc.function_type_container[desc] = f

        if s.te_visit(tc, f) is False:
            tc.logger.log(f"Cant infer statement"+
                f"at line {s.linespan[0]}!", 
                    LogTypes.FUNCTION_RESOLUTION)
            cleanup()
            return None

    if not ret_done:
        f.types["return"] = self.expr_ret.te_visit(tc, f)
        if f.types["return"] is None:
            tc.logger.log("Cant infer return type!", 
                    LogTypes.FUNCTION_RESOLUTION)
            cleanup()
            return None
        ret_done = True
        # for recursive calls, statements are not needed
        tc.function_type_container[desc] = f

    cleanup()
    return f


@add_method_te_visit(sa.StructDefinition)
def _(self: sa.StructDefinition, tc: TC,
      type_args: List[ts.Type],
      ):
    tc.logger.go_in()
    tc.logger.log(f"Struct definition at {self.linespan[0]}", 
            LogTypes.FUNCTION_DEFINITION)
    s = ts.StructType(self.name)

    s.types = dict([
        a for a in zip(self.type_parameter_names, type_args)
    ])

    for stat in self.statement_list:
        if stat.te_visit(tc, s) is False:
            tc.logger.log(f"Cant infer statement"+
                            f"at line {stat.linespan[0]}!", 
                    LogTypes.STRUCT_RESOLUTION)
            tc.logger.go_out()
            return None

    s.mangled_name = tc.scope_man.new_struct_name(self.name)

    tc.logger.go_out()
    return s


# function statements

@add_method_te_visit(sa.BlockStatement)
def _(self: sa.BlockStatement, tc: TC,
        f: ts.FunctionType):
    tc.scope_man.begin_scope()
    for s in self.statement_list:
        if self.expr.te_visit(tc, f) is False:
            tc.scope_man.end_scope()
            return False

    tc.scope_man.end_scope()
    return True


@add_method_te_visit(sa.ExpressionStatement)
def _(self: sa.ExpressionStatement, tc: TC,
        f: ts.FunctionType):
    if self.expr.te_visit(tc, f) is None:
        return False
    return True


@add_method_te_visit(sa.TypeDeclarationStatementFunction)
def _(self: sa.TypeDeclarationStatementFunction, tc: TC,
        f: ts.FunctionType):
    mn = tc.scope_man.new_var_name(self.name, type_name=True)
    f.types[mn] = self.type_expr.te_visit(tc, f)
    if f.types[mn] is None:
        return False
    return True


@add_method_te_visit(sa.AssignmentStatement)
def _(self: sa.AssignmentStatement, tc: TC,
        f: ts.FunctionType):

    le = self.left.te_visit(tc, f)
    if not self.left.lvalue:
        raise RuntimeError("Require lvalue at {self.linespan[0]}!")
    if le is None: return False

    re = self.right.te_visit(tc, f)
    if re is None: return False

    if f.types[le] != f.types[re]:
        tc.logger.log("type missmatch at {self.linespan[0]}",
                LogTypes.TYPE_MISSMATCH)
        return False
    else:
        copy = tc.resolve_function("__copy__",[],
            [ts.PointerType(f.types[le]), ts.PointerType(f.types[re])]
        )
        if copy is None:
            tc.logger.log("dont have copy for assignment at {self.linespan[0]}",
                    LogTypes.TYPE_MISSMATCH)
            return False
            
        d = tc.scope_man.new_tmp_var_name("copy dummy")

        f.flat_statements.append(ir.FunctionCall(d, 
            copy.mangled_name, [le, re]))
        return True


@add_method_te_visit(sa.InitStatement)
def _(self: sa.InitStatement, tc: TC,
        f: ts.FunctionType):
    mn = tc.scope_man.new_var_name(self.name)

    e = self.expr.te_visit(tc, f)
    if e is None: return False

    if f.types[e] is ts.VoidType():
        return True

    f.types[mn] = f.types[e]
    f.flat_statements.append(ir.MemoryCopy(mn, e))
    return True


@add_method_te_visit(sa.WhileStatement)
def _(self: sa.WhileStatement, tc: TC,
        f: ts.FunctionType):
    lwc = tc.scope_man.new_label_name("while check")
    lwe = tc.scope_man.new_label_name("while end")
    f.break_label_stack.append(lwe)

    tc.scope_man.begin_scope()

    ec = self.expr_check.te_visit(tc, f)
    if ec is None or not isinstance(f.types[ec],ts.BoolType):
        tc.logger.log(f"check expr must be bool\
                at {self.expr_check.lineno[0]}", 
                LogTypes.RUNTIME_EXPR_ERROR)
        tc.scope_man.end_scope()
        f.break_label_stack.pop()
        return False

    f.flat_statements.append(ir.Label(lwc))
    f.flat_statements.append(ir.JumpToLabelFalse(ec, lwe))
    for s in self.statement_list:
        if s.te_visit(tc, f) is False:
            tc.scope_man.end_scope()
            f.break_label_stack.pop()
            return False

    f.flat_statements.append(ir.Label(lwe))

    tc.scope_man.end_scope()
    f.break_label_stack.pop()
    return True


@add_method_te_visit(sa.ForStatement)
def _(self: sa.ForStatement, tc: TC,
        f: ts.FunctionType):
    lfcheck = tc.scope_man.new_label_name("for check")
    lfchange = tc.scope_man.new_label_name("for change")
    lfe = tc.scope_man.new_label_name("for end")
    f.break_label_stack.append(lfe)

    tc.scope_man.begin_scope()

    if self.stat_init.te_visit(tc, f) is False: return False

    f.flat_statements.append(ir.Label(lfcheck))

    ec = self.expr_check.te_visit(tc, f)
    if ec is None: return False

    if not isinstance(f.types[ec], ts.BoolType):
        tc.logger.log(f"check expr must be bool\
                at {self.expr_check.lineno[0]}", 
                LogTypes.RUNTIME_EXPR_ERROR)
        tc.scope_man.end_scope()
        f.break_label_stack.pop()
        return False

    f.flat_statements.append(ir.JumpToLabelFalse(ec, lfe))
    for s in self.statement_list:
        if s.te_visit(tc, f) is False:
            tc.scope_man.end_scope()
            f.break_label_stack.pop()
            return False

    f.flat_statements.append(ir.Label(lfchange))
    if self.stat_change.te_visit(tc, f) is False:
        tc.scope_man.end_scope()
        f.break_label_stack.pop()
        return False

    f.flat_statements.append(ir.JumpToLabel(lfcheck))

    tc.scope_man.end_scope()
    f.break_label_stack.pop()
    return True


@add_method_te_visit(sa.IfElseStatement)
def _(self: sa.IfElseStatement, tc: TC,
        f: ts.FunctionType):
    iftrue = tc.scope_man.new_label_name("if true")
    iffalse = tc.scope_man.new_label_name("if false")
    ifend = tc.scope_man.new_label_name("if end")

    tc.scope_man.begin_scope()
    ec = self.expr_check.te_visit(tc, f)
    if ec is None: return False

    if not isinstance(f.types[ec], ts.BoolType):
        tc.logger.log(f"check expr must be bool\
                at {self.expr_check.lineno[0]}", 
                LogTypes.RUNTIME_EXPR_ERROR)
        tc.scope_man.end_scope()
        return False

    f.flat_statements.append(ir.JumpToLabelFalse(ec, iffalse))
    f.flat_statements.append(ir.Label(iftrue))
    for s in self.statement_list_false:
        if s.te_visit(tc, f) is False:
            return False

    f.flat_statements.append(ir.JumpToLabel(ec, ifend))
    f.flat_statements.append(ir.Label(iffalse))
    for s in self.statment_list_false:
        if s.te_visit(tc, f) is False:
            return False

    f.flat_statements.append(ir.Label(ifend))
    tc.scope_man.end_scope()
    return True


@add_method_te_visit(sa.ReturnStatement)
def _(self: sa.ReturnStatement, tc: TC,
        f: ts.FunctionType):
    if self.expr is None:
        if f.types["return"]!=ts.VoidType():
            tc.logger.log("type missmatch with return {self.linespan[0]}",
                    LogTypes.TYPE_MISSMATCH)
            return False
        f.flat_statements.append(ir.FunctionReturn(None))
        return True
    else:
        e = self.expr.te_visit(tc, f)
        if e is None: return False

        print(f.name)
        print(e)
        print(f.types)
        if f.types[e] != f.types["return"]:
            tc.logger.log("type missmatch with return {self.linespan[0]}",
                    LogTypes.TYPE_MISSMATCH)
            return False

        f.flat_statements.append(ir.FunctionReturn(e))
        return True


@add_method_te_visit(sa.BreakStatement)
def _(self: sa.BreakStatement, tc: TC,
        f: ts.FunctionType):
    if self.no <= 0:
        raise RuntimeError("break must be >0")
    if self.no > len(f.break_label_stack):
        raise RuntimeError("dont have enough \
                loops to break out of")

    f.flat_statements.append(ir.JumpToLabel(
        f.break_label_stack[len(f.break_label_stack)-self.no]
    ))
    return True


# struct statements


@add_method_te_visit(sa.MemberDeclarationStatement)
def _(self: sa.MemberDeclarationStatement, tc: TC,
        s: ts.StructType):
    t = self.type_expr.te_visit(tc, s)
    if t is None:
        return False
    if self.name in s.types:
        raise RuntimeError(f"redefinition of name {self.name}")

    s.types[self.name] = t
    s.members.append(self.name)
    return True


@add_method_te_visit(sa.TypeDeclarationStatementStruct)
def _(self: sa.TypeDeclarationStatementStruct, tc: TC,
        s: ts.StructType):
    t = self.type_expr.te_visit(tc, s)
    if t is None:
        return False
    if self.name in s.types:
        raise RuntimeError(f"redefinition of name {self.name}")
    s.types[self.name] = t
    return True


# value expressions

@add_method_te_visit(sa.IdExpression)
def _(self: sa.IdExpression, tc: TC,
        f: ts.FunctionType):
    self.lvalue = True
    tmp = tc.scope_man.get_var_name(self.name)
    return tmp


@add_method_te_visit(sa.BinaryExpression)
def _(self: sa.BinaryExpression, tc: TC,
        f: ts.FunctionType):
    self.lvalue = False

    le = self.left.te_visit(tc, f)
    if not self.left.lvalue:
        raise RuntimeError("Require lvalue at {self.linespan[0]}!")
    if le is None: return None

    re = self.right.te_visit(tc, f)
    if re is None: return None

    tmp = tc.scope_man.new_tmp_var_name(f"{self.op}")

    opf = tc.resolve_function(self.op, [], [f.types[le], f.types[re]])
    if opf is None:
        tc.logger.log("cant resolve op at {self.linespan[0]}",
                LogTypes.FUNCTION_RESOLUTION)
        return None

    f.flat_statements.append(ir.FunctionCall(
        tmp, opf.mangled_name, [le, re]))
    f.types[tmp] = opf.types["return"]
    return tmp


@add_method_te_visit(sa.BracketCallExpression)
def _(self: sa.BracketCallExpression, tc: TC,
        f: ts.FunctionType):
    self.lvalue = True

    e = self.expr.te_visit(tc, f)
    if not e.lvalue:
        raise RuntimeError("Require lvalue at {self.linespan[0]}!")
    if e is None: return None

    ind = self.index.te_visit(tc, f)
    if ind is None: return None

    if not isinstance(f.types[ind], ts.IntType):
        tc.logger.log(f"cant index with nonint type at\
                {self.ind.linespan[0]}", 
                LogTypes.RUNTIME_EXP)

    tmp = tc.scope_man.new_tmp_var_name("bracket call")
    f.types[tmp] = f.types[e]

    f.flat_statements.append(ir.GetPointerOffset(tmp, e, ind))
    return tmp


@add_method_te_visit(sa.MemberIndexExpression)
def _(self: sa.MemberIndexExpression, tc: TC,
        f: ts.FunctionType):
    self.lvalue = True

    e = self.expr.te_visit(tc, f)
    if not self.expr.lvalue:
        raise RuntimeError("Require lvalue at {self.linespan[0]}!")
    if e is None: return None

    if not isinstance(f.types[e], ts.StructType):
        tc.logger.log(f"cant refer to a member of a non struct type at\
                {self.expr.linespan[0]}",
                LogTypes.TYPE_MISSMATCH)
        return None

    tmp = tc.scope_man.new_tmp_var_name("member index")
    if self.member not in f.types[e].members:
        tc.logger.log(f"cant refer to nonexistant member\
                {self.expr.linespan[0]}",
                LogTypes.TYPE_MISSMATCH)
        return None

    f.types[tmp] = f.types[e].types[self.member]
    f.flat_statements.append(ir.GetElementPtr(tmp, e, self.member))
    return tmp


@add_method_te_visit(sa.DerefExpression)
def _(self: sa.DerefExpression, tc: TC,
        f: ts.FunctionType):
    e = self.expr.te_visit(tc, f)
    if e is None: return None
    self.lvalue = self.expr.lvalue

    if not isinstance(f.types[e], ts.PointerType):
        tc.logger.log(f"cant deref non pointer type at"+
                f"{self.expr.linespan[0]}",
                LogTypes.TYPE_MISSMATCH)
        return None

    tmp = tc.scope_man.new_tmp_var_name("ptr deref")
    f.types[tmp] = f.types[e].pointed
    f.flat_statements.append(ir.Dereference(tmp, e))
    return tmp


@add_method_te_visit(sa.AddressExpression)
def _(self: sa.BinaryExpression, tc: TC,
        f: ts.FunctionType):
    self.lvalue = False

    e = self.expr.te_visit(tc, f)
    if not self.expr.lvalue:
        raise RuntimeError("Require lvalue at {self.linespan[0]}!")
    if e is None: return None

    tmp = tc.scope_man.new_tmp_var_name("addr of")
    f.types[tmp] = ts.PointerType(f.types[e])
    f.flat_statements.append(ir.AddressOf(tmp, e))
    return tmp


@add_method_te_visit(sa.IntLiteralExpression)
def _(self: sa.IntLiteralExpression, tc: TC,
        f: ts.FunctionType):
    self.lvalue = False

    tmp = tc.scope_man.new_tmp_var_name("int literal")
    f.types[tmp] = ts.IntType(self.size)
    f.flat_statements.append(ir.IntConstantAssignment(tmp,
                                                      self.value,
                                                      self.size))
    return tmp


@add_method_te_visit(sa.BoolLiteralExpression)
def _(self: sa.BoolLiteralExpression, tc: TC,
        f: ts.FunctionType):
    self.lvalue = False

    tmp = tc.scope_man.new_tmp_var_name("bool literal")
    f.types[tmp] = ts.BoolType()
    f.flat_statements.append(ir.BoolConstantAssignment(tmp,
                                                       self.value))
    return tmp


@add_method_te_visit(sa.CallExpression)
def _(self: sa.CallExpression, tc: TC,
        f: ts.FunctionType):
    self.lvalue = False

    tmp = tc.scope_man.new_tmp_var_name("bool literal")

    type_args_types = [t.te_visit(tc, f) for t in self.type_expr_list]
    if None in type_args_types: return None

    args = [v.te_visit(tc, f) for v in self.args]
    if None in args: return None

    args_types = [f.types[a] for a in args]

    ft = tc.resolve_function(self.name, type_args_types, args_types)
    if ft is not None:
        f.flat_statements.append(ir.FunctionCall(tmp,
                                                 ft.mangled_name,
                                                 args))
        f.types[tmp] = ft.types["return"]
    else:
        st = tc.resolve_struct(self.name, type_args_types)
        if st is None:
            return None

        f.types[tmp] = st

        ft = tc.resolve_function(
            "__init__", [], [ts.PointerType(st)]+args_types)
        if ft is None:
            return None
        vd = tc.scope_man.new_tmp_var_name("void dummy")
        f.flat_statements.append(ir.FunctionCall(vd,
                                                 ft.mangled_name,
                                                 [tmp]+args))
        f.types[vd] = ft.types["return"]
        st.needs_gen = True
    return tmp



# type expressions

@add_method_te_visit(sa.TypeBinaryExpression)
def _(self: sa.TypeBinaryExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):

    le = self.left.te_visit(tc, sf)
    if le is None: return None

    re = self.right.te_visit(tc, sf)
    if re is None: return None

    rt = tc.resolve_struct(self.op, [le, re])
    if rt is None:
        tc.logger.log(f"[ERR] Can't infer for op {self.op}!",
                LogTypes.FUNCTION_OR_STRUCT_DEFINITION)
        return None

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
    if None in texprs: return None

    rt = tc.resolve_struct(self.name, texprs)
    if rt is None:
        tc.logger.log(f"[ERR] Can't infer type {self.name}!",
                LogTypes.FUNCTION_OR_STRUCT_DEFINITION)
        return None

    return rt

@add_method_te_visit(sa.TypeIdExpression)
def _(self: sa.TypeIdExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):

    if self.name in sf.types:
        return sf.types[self.name]
    elif isinstance(sf, ts.FunctionType):
        mn = tc.scope_man.get_var_name(self.name)
        if mn is not None:
            return sf.types[mn]

    rt = tc.resolve_struct(self.name, [])
    if rt is None:
        tc.logger.log(f"[ERR] Can't infer type {self.name}!",
                LogTypes.FUNCTION_OR_STRUCT_DEFINITION)
        return None

    return rt

@add_method_te_visit(sa.TypeTypeExpression)
def _(self: sa.TypeTypeExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):
    return self.type_obj

@add_method_te_visit(sa.TypeDerefExpression)
def _(self: sa.TypeDerefExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionType]):

    e = self.expr.te_visit(tc, sf)
    if e is None: return None

    if isinstance(e, ts.PointerType):
        return e.pointed
    else:
        tc.logger.log(f"[ERR] Can't deref non pointer!",
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
        tc.logger.log(f"[ERR] TypeIndexExpression must be on struct!",
                LogTypes.FUNCTION_OR_STRUCT_DEFINITION)
        return None
    return e.types[self.name]


#### SPECIALS

@add_method_te_visit(sa.MemoryCopyStatement)
def _(self: sa.MemoryCopyStatement, tc: TC,
        f: ts.FunctionType):
    d = self.dest
    s = self.src
    f.flat_statements.append(ir.MemoryCopy(d, s))
    return True

@add_method_te_visit(sa.PrimitiveCallExpression)
def _(self: sa.PrimitiveCallExpression, tc: TC,
        f: ts.FunctionType):
    self.lvalue = False

    args = [v.te_visit(tc, f) for v in self.args]
    if None in args: return None

    tmp = tc.scope_man.new_tmp_var_name("primitive call")
    f.flat_statements.append(ir.FunctionCall(tmp, self.mangled_name, args))
    print("A: "+tmp)
    f.types[tmp] = self.return_type 
    return tmp
