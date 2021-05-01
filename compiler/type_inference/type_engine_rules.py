from typing import List, Union, Any

from . import flat_ir as ir
from ..helpers import add_method_te_visit
from ..semantics_parsing import semantic_ast as sa

from .type_engine import TypingContext as TC
from .type_engine import LogTypes 

from . import type_system as ts

# utils for type_engine_rules

def new_tmp_stack_symbolic_register_unallocated(f: ts.FunctionTypeNormal, tc: TC, ty: ts.Type, desc: str = ""):
    mn = tc.scope_man.new_tmp_var_name(desc, type_name = False)
    f.types[mn] = ty
    return mn

def new_tmp_stack_symbolic_register(f: ts.FunctionTypeNormal, tc: TC, ty: ts.Type, desc: str = ""):
    mn = tc.scope_man.new_tmp_var_name(desc, type_name = False)
    f.types[mn] = ty
    f.flat_statements.append(ir.StackAllocate(mn))
    return mn

def new_stack_symbolic_register(f: ts.FunctionTypeNormal, tc: TC, ty: ts.Type, name: str):
    mn = tc.scope_man.new_var_name(name, type_name = False)
    f.types[mn] = ty
    f.flat_statements.append(ir.StackAllocate(mn))
    return mn

def get_stack_symbolic_register(f: ts.FunctionTypeNormal, tc: TC, name: str):
    return tc.scope_man.get_var_name(name)

def add_func_call(self, f: ts.FunctionTypeNormal, tc: TC, 
        fn_to_call: ts.FunctionType, args_names, args_lvalues, desc: str):
    if isinstance(fn_to_call, ts.FunctionTypeDoNothing):
        return None

    retty = fn_to_call.types["return"]

    if retty != ts.VoidType():
        ret_reg = new_tmp_stack_symbolic_register(f, tc, retty, desc)
    else:
        ret_reg = None

    types = [f.types[n] for n in args_names] 

    copied_args_names = []
    for i in range(len(args_names)):
        if not args_lvalues[i] or f.do_not_copy_args:
            copied_args_names.append(args_names[i])
        else:
            tmp = new_stack_symbolic_register(f, tc, ty, args_names[i]+"_copy")
            fn_copy = tc.resolve_function("__copy__", [], [ts.PointerType(types[i])]*2)
            add_func_call(
                    f, 
                    tc, 
                    fn_copy, 
                    [tmp, args_names[i]], 
                    [False, False], 
                    False,
                    "copy_call"
            )
            copied_args_names.append(tmp)

    f.flat_statements.append(ir.FunctionCall(ret_reg, fn_to_call.mangled_name, retty.mangled_name, copied_args_names))
            
    return ret_reg


# structural

@add_method_te_visit(sa.Program)
def _(self: sa.Program, tc: TC):
    raise RuntimeError("this is not parsed directly")


@add_method_te_visit(sa.FunctionDefinition)
def _(self: sa.FunctionDefinition, tc: TC,
      type_args_types: List[ts.Type],
      args_types: List[ts.Type],
      ) -> Any:
    desc = (
        self.name,
        tuple(type_args_types),
        tuple(args_types)
    )
    tc.scope_man.begin_scope()
    tc.logger.go_in()
    tc.logger.log(f"Function definition at {self.linespan[0]}", 
            LogTypes.FUNCTION_DEFINITION)

    def cleanup_fail():
        tc.scope_man.end_scope()
        if desc in tc.function_type_container:
            tc.function_type_container.pop(desc)
        tc.logger.go_out()

    def infer_ret_type():
        retty = self.expr_ret.te_visit(tc, f)
        if retty is None:
            tc.logger.log("Cant infer return type!", 
                    LogTypes.FUNCTION_RESOLUTION)
            return False

        tc.function_type_container[desc] = f
        f.types["return"] = retty
        if retty != ts.VoidType():
            f.flat_statements.append(ir.StackAllocate("return"))
        return True

    f = ts.FunctionTypeNormal(self.name)
    f.mangled_name = tc.scope_man.new_func_name(self.name)

    # type params
    for name, t in zip(self.type_parameter_names, type_args_types):
        n = tc.scope_man.new_var_name(name, type_name=True)
        f.types[n] = t

    # params
    for name, t in zip(self.parameter_names, args_types):
        n = new_stack_symbolic_register(f, tc, t, name)

        pp = "param_placeholder"+n
        f.parameter_names_ordered.append(pp)
        print(pp)
        f.types[pp] = t

        f.flat_statements.append(ir.StackStore(n, pp))
        if f.dest_params:
            tc.scope_man.add_to_dest(n)


    f.flat_statements.append(ir.Comment("func setup done"))

    for s in self.statement_list:
        if not "return" in f.types and not isinstance(s, sa.TypeDeclarationStatementFunction):
            if not infer_ret_type():
                cleanup_fail()
                return None

        if s.te_visit(tc, f) is False:
            tc.logger.log(f"Cant infer statement"+
                f"at line {s.linespan[0]}!", 
                    LogTypes.FUNCTION_RESOLUTION)
            cleanup_fail()
            return None

    if not "return" in f.types:
        if not infer_ret_type():
            cleanup_fail()
            return None

    # destruct and return
    f.flat_statements.append(ir.JumpToLabel("func_end"))
    f.flat_statements.append(ir.Label("func_end"))

    for td in tc.scope_man.get_dest_list():
        fn_dest = tc.resolve_function("__dest__", [], [ts.PointerType(f.types[td])])
        add_func_call(
                f, 
                tc, 
                fn_dest, 
                [td], 
                [False], 
                "dest_call"
        )
    f.flat_statements.append(ir.FunctionReturn())

    tc.scope_man.end_scope()
    tc.logger.go_out()
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
        f: ts.FunctionTypeNormal):
    tc.scope_man.begin_scope()
    for s in self.statement_list:
        if self.expr.te_visit(tc, f) is False:
            tc.scope_man.end_scope()
            return False

    for td in tc.scope_man.get_dest_list():
        add_dest(self,f,tc,td)
    tc.scope_man.end_scope()
    return True


@add_method_te_visit(sa.ExpressionStatement)
def _(self: sa.ExpressionStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    e = self.expr.te_visit(tc, f)
    if e is None:
        return False
    if not self.expr.lvalue:
        add_dest(self, f, tc, e)
    return True


@add_method_te_visit(sa.TypeDeclarationStatementFunction)
def _(self: sa.TypeDeclarationStatementFunction, tc: TC,
        f: ts.FunctionTypeNormal):
    mn = tc.scope_man.new_var_name(self.name, type_name=True)
    f.types[mn] = self.type_expr.te_visit(tc, f)
    if f.types[mn] is None:
        return False
    return True


@add_method_te_visit(sa.AssignmentStatement)
def _(self: sa.AssignmentStatement, tc: TC,
        f: ts.FunctionTypeNormal):

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
        # destroy left side
        if not add_dest(self, f, tc, le): return False

        # copy or memory copy
        if self.right.lvalue:
            if not add_copy(self, f, tc, le, re): return False
        else:
            f.flat_statements.append(ir.StackCopy(le, re))

        return True


@add_method_te_visit(sa.InitStatement)
def _(self: sa.InitStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    mn = tc.scope_man.new_var_name(self.name)
    tc.scope_man.add_to_dest(mn)

    e = self.expr.te_visit(tc, f)
    if e is None: return False
    f.types[mn] = f.types[e]

    # what was this? TODO
    #if f.types[e] is ts.VoidType():
    #    return True
    f.flat_statements.append(ir.StackAllocate(mn))

    if self.expr.lvalue:
        if not add_copy(self, f, tc, mn, e): return False
    else:
        f.flat_statements.append(ir.StackCopy(mn, e))

    return True


@add_method_te_visit(sa.WhileStatement)
def _(self: sa.WhileStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    lwc = tc.scope_man.new_label_name("while check")
    lws = tc.scope_man.new_label_name("while succ")
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
    f.flat_statements.append(ir.JumpToLabelConditional(ec, lws, lwe))
    f.flat_statements.append(ir.Label(lws))
    for s in self.statement_list:
        if s.te_visit(tc, f) is False:
            tc.scope_man.end_scope()
            f.break_label_stack.pop()
            return False

    f.flat_statements.append(ir.Label(lwe))
    if not self.expr_check.lvalue:
        if not add_dest(self, f, tc, ec): return False

    
    for td in tc.scope_man.get_dest_list():
        add_dest(self,f,tc,td)
    tc.scope_man.end_scope()
    f.break_label_stack.pop()
    return True


@add_method_te_visit(sa.ForStatement)
def _(self: sa.ForStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    lfcheck = tc.scope_man.new_label_name("for_check")
    lfsucc = tc.scope_man.new_label_name("for_succ")
    lfchange = tc.scope_man.new_label_name("for_change")
    lfe = tc.scope_man.new_label_name("for_end")
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

    f.flat_statements.append(ir.JumpToLabelConditional(ec, lfsucc, lfe))
    f.flat_statements.append(ir.Label(lfsucc))
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
    if not self.expr_check.lvalue:
        if not add_dest(self, f, tc, ec): return False

    for td in tc.scope_man.get_dest_list():
        add_dest(self,f,tc,td)
    tc.scope_man.end_scope()
    f.break_label_stack.pop()
    return True


@add_method_te_visit(sa.IfElseStatement)
def _(self: sa.IfElseStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    iftrue = tc.scope_man.new_label_name("if_true")
    iffalse = tc.scope_man.new_label_name("if_false")
    ifend = tc.scope_man.new_label_name("if_end")

    tc.scope_man.begin_scope()
    ec = self.expr_check.te_visit(tc, f)
    if ec is None: return False

    if not isinstance(f.types[ec], ts.BoolType):
        tc.logger.log(f"check expr must be bool\
                at {self.expr_check.lineno[0]}", 
                LogTypes.RUNTIME_EXPR_ERROR)
        tc.scope_man.end_scope()
        return False

    f.flat_statements.append(ir.JumpToLabelConditional(ec, iftrue, iffalse))
    f.flat_statements.append(ir.Label(iftrue))
    for s in self.statement_list_false:
        if s.te_visit(tc, f) is False:
            return False
    f.flat_statements.append(ir.JumpToLabel(ifend))

    f.flat_statements.append(ir.Label(iffalse))
    for s in self.statement_list_false:
        if s.te_visit(tc, f) is False:
            return False

    f.flat_statements.append(ir.Label(ifend))
    if not self.expr_check.lvalue:
        if not add_dest(self, f, tc, ec): return False

    for td in tc.scope_man.get_dest_list():
        add_dest(self,f,tc,td)
    tc.scope_man.end_scope()
    return True


@add_method_te_visit(sa.ReturnStatement)
def _(self: sa.ReturnStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    if self.expr is None:
        if f.types["return"]!=ts.VoidType():
            tc.logger.log("type missmatch with return {self.linespan[0]}",
                    LogTypes.TYPE_MISSMATCH)
            return False
        f.flat_statements.append(ir.JumpToLabel("func_end"))
        return True
    else:
        e = self.expr.te_visit(tc, f)
        if e is None: return False

        if f.types[e] != f.types["return"]:
            tc.logger.log("type missmatch with return {self.linespan[0]}",
                    LogTypes.TYPE_MISSMATCH)
            return False

        f.flat_statements.append(ir.StackCopy("return", e))
        f.flat_statements.append(ir.JumpToLabel("func_end"))
        return True


@add_method_te_visit(sa.BreakStatement)
def _(self: sa.BreakStatement, tc: TC,
        f: ts.FunctionTypeNormal):
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
        f: ts.FunctionTypeNormal):
    self.lvalue = True
    tmp = get_stack_symbolic_register(f, tc, name)
    return tmp


@add_method_te_visit(sa.BracketCallExpression)
def _(self: sa.BracketCallExpression, tc: TC,
        f: ts.FunctionTypeNormal):
    self.lvalue = True

    e = self.expr.te_visit(tc, f)
    if e is None: return None
    if not isinstance(f.types[e], ts.PointerType):
        tc.logger.log(f"cant index non-ptr type at\
                {self.e.linespan[0]}", 
                LogTypes.RUNTIME_EXP)

    if not self.expr.lvalue:
        raise RuntimeError("Require lvalue at {self.linespan[0]}!")

    ind = self.index.te_visit(tc, f)
    if ind is None: return None
    if not isinstance(f.types[ind], ts.IntType):
        tc.logger.log(f"cant index with non-int type at\
                {self.ind.linespan[0]}", 
                LogTypes.RUNTIME_EXP)

    tmp = new_tmp_stack_symbolic_register(f, tc, f.types[e], "bracket_call")
    f.flat_statements.append(ir.GetPointerOffset(tmp, e, ind, f.types[ind].size))

    return tmp


@add_method_te_visit(sa.MemberIndexExpression)
def _(self: sa.MemberIndexExpression, tc: TC,
        f: ts.FunctionTypeNormal):
    self.lvalue = True

    e = self.expr.te_visit(tc, f)
    if not self.expr.lvalue:
        raise RuntimeError(f"Require lvalue at {self.linespan[0]}!")
    if e is None: return None

    if not isinstance(f.types[e], ts.StructType):
        tc.logger.log(f"cant refer to a member of a non struct type at\
                {self.expr.linespan[0]}",
                LogTypes.TYPE_MISSMATCH)
        return None

    if self.member not in f.types[e].members:
        tc.logger.log(f"cant refer to nonexistant member\
                {self.expr.linespan[0]}",
                LogTypes.TYPE_MISSMATCH)
        return None

    tmp = new_tmp_stack_symbolic_register_unallocated(f, tc, f.types[e].types[self.member], "member_index")
    f.flat_statements.append(ir.GetElementPtr(tmp, e, self.member))

    return tmp


@add_method_te_visit(sa.DerefExpression)
def _(self: sa.DerefExpression, tc: TC,
        f: ts.FunctionTypeNormal):
    e = self.expr.te_visit(tc, f)
    if e is None: return None

    if not isinstance(f.types[e], ts.PointerType):
        tc.logger.log(f"cant deref non pointer type at"+
                f"{self.expr.linespan[0]}",
                LogTypes.TYPE_MISSMATCH)
        return None

    self.lvalue = self.expr.lvalue

    tmp = new_tmp_stack_symbolic_register_unallocated(f, tc, f.types[e].pointed, "deref")
    f.flat_statements.append(ir.Dereference(tmp, e))

    return tmp


@add_method_te_visit(sa.AddressExpression)
def _(self: sa.BinaryExpression, tc: TC,
        f: ts.FunctionTypeNormal):
    self.lvalue = False

    e = self.expr.te_visit(tc, f)
    if not self.expr.lvalue:
        raise RuntimeError(f"Require lvalue at {self.linespan[0]}!")
    if e is None: return None

    tmp - new_tmp_stack_symbolic_register(f, tc, ts.PointerType(f.types[e]), "addrof")
    f.flat_statements.append(ir.AddressOf(tmp, e))

    return tmp


@add_method_te_visit(sa.IntLiteralExpression)
def _(self: sa.IntLiteralExpression, tc: TC,
        f: ts.FunctionTypeNormal):
    self.lvalue = False

    tmp = new_tmp_stack_symbolic_register(f, tc, ts.IntType(self.size), "int_lit")
    f.flat_statements.append(ir.IntConstantAssignment(tmp,
                                                      self.value,
                                                      self.size))
    return tmp


@add_method_te_visit(sa.BoolLiteralExpression)
def _(self: sa.BoolLiteralExpression, tc: TC,
        f: ts.FunctionTypeNormal):
    self.lvalue = False

    tmp = new_tmp_stack_symbolic_register(f, tc, ts.BoolType(), "bool_lit")
    f.flat_statements.append(ir.BoolConstantAssignment(tmp,
                                                       self.value))
    return tmp


@add_method_te_visit(sa.CallExpression)
def _(self: sa.CallExpression, tc: TC,
        f: ts.FunctionTypeNormal):
    self.lvalue = False

    type_args_types = [t.te_visit(tc, f) for t in self.type_expr_list]
    if None in type_args_types: return None

    arg_names = [v.te_visit(tc, f) for v in self.args]
    if None in arg_names: return None

    args_types = [f.types[a] for a in arg_names]

    func_call = tc.resolve_function(self.name, type_args_types, args_types)
    copy_bools = [t.lvalue for t in self.type_expr_list]

    if func_call is not None:
        ret = add_func_call(f, tc, func_call, arg_names, copy_bools, True, "call")
        return ret
    else:
        struct = tc.resolve_struct(self.name, type_args_types)
        if struct is None:
            return None

        init_call = tc.resolve_function("__init__", [], [ts.PointerType(st)]+args_types)
        if init_call is None:
            return None

        newo = new_tmp_stack_symbolic_register(f, tc, struct, "newo")
        newo_ptr = new_tmp_stack_symbolic_register(f, tc, ts.PointerType(struct), "ptr_to_newo")
        f.flat_statements.append(ir.AddressOf(newo_ptr, newo))

        add_func_call(f, tc, init_call, [newo_ptr]+arg_names, [False]+copy_bools, True, "init_call")

        st.needs_gen = True
        return reg


# type expressions

@add_method_te_visit(sa.TypeBinaryExpression)
def _(self: sa.TypeBinaryExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

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
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

    if len(self.expr_list) == 0:
        if isinstance(sf, ts.StructType):
            if self.name in sf.types:
                return sf.types[self.name]
        elif isinstance(sf, ts.FunctionTypeNormal):
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
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

    if self.name in sf.types:
        return sf.types[self.name]
    elif isinstance(sf, ts.FunctionTypeNormal):
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
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):
    return self.type_obj

@add_method_te_visit(sa.TypeDerefExpression)
def _(self: sa.TypeDerefExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

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
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

    e = self.expr.te_visit(tc, sf)
    if e is None: return None

    return ts.PointerType(e)


@add_method_te_visit(sa.TypeIndexExpression)
def _(self: sa.TypeIndexExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

    e = self.expr.te_visit(tc, sf)
    if e is None: return None

    if not isinstance(e, ts.StructType):
        tc.logger.log(f"[ERR] TypeIndexExpression must be on struct!",
                LogTypes.FUNCTION_OR_STRUCT_DEFINITION)
        return None
    return e.types[self.name]

