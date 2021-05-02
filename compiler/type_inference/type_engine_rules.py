from typing import List, Union, Any

from . import flat_ir as ir
from ..helpers import add_method_te_visit
from ..semantics_parsing import semantic_ast as sa

from .type_engine import TypingContext as TC

from . import type_system as ts
from . import inference_errors as ierr

# utils for type_engine_rules

def new_tmp_stack_symbolic_register_unallocated(f: ts.FunctionTypeNormal, tc: TC, ty: ts.Type, desc: str):
    mn = tc.scope_man.new_tmp_var_name(desc, type_name = False)
    f.types[mn] = ty
    return mn

def new_tmp_stack_symbolic_register(f: ts.FunctionTypeNormal, tc: TC, ty: ts.Type, desc: str):
    mn = tc.scope_man.new_tmp_var_name(desc, type_name = False)
    f.types[mn] = ty
    f.flat_statements.append(ir.StackAllocate(mn))
    return mn

def new_stack_symbolic_register(sa_node, f: ts.FunctionTypeNormal, tc: TC, ty: ts.Type, name: str):
    mn = tc.scope_man.new_var_name(name, type_name = False)
    if mn is None:
        raise ierr.RuntimeExpressionError(f"Name duplication ({name}), at {sa_node.linespan[0]}!")
    f.types[mn] = ty
    f.flat_statements.append(ir.StackAllocate(mn))
    return mn

def get_stack_symbolic_register(sa_node, f: ts.FunctionTypeNormal, tc: TC, name: str):
    mn = tc.scope_man.get_var_name(name)
    if mn is None:
        raise ierr.RuntimeExpressionError(f"Variable {name} not defined, at {sa_node.linespan[0]}!")
    return mn

def add_func_call(sa_node, f: ts.FunctionTypeNormal, tc: TC, 
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
            copy_reg = new_tmp_stack_symbolic_register(f, tc, types[i], args_names[i]+"_copy")
            add_copy(sa_node, f, tc, copy_reg, args_names[i])
            copied_args_names.append(copy_reg)

    f.flat_statements.append(ir.FunctionCall(ret_reg, fn_to_call.mangled_name, retty.mangled_name, copied_args_names))
            
    return ret_reg

def add_dest(sa_node, f: ts.FunctionTypeNormal, tc, name: str):
    """
    Expects a stack symbolic registers with type s.
    """
    ptr_name = new_tmp_stack_symbolic_register(f, tc, ts.PointerType(f.types[name]), name+"_destptr")
    f.flat_statements.append(ir.AddressOf(ptr_name, name))

    fn_dest = tc.resolve_function("__dest__", [], [ts.PointerType(f.types[name])])
    add_func_call(
            sa_node,
            f, 
            tc, 
            fn_dest, 
            [ptr_name], 
            [False], 
            "dest_call"
    )

def add_copy(sa_node, f: ts.FunctionTypeNormal, tc, dst: str, src: str):
    """
    Expects two stack symbolic registers with type s.
    """
    ptr_src = new_tmp_stack_symbolic_register(f, tc, ts.PointerType(f.types[src]), src+"_srcptr")
    ptr_dst = new_tmp_stack_symbolic_register(f, tc, ts.PointerType(f.types[dst]), dst+"_dstptr")

    f.flat_statements.append(ir.AddressOf(ptr_src, src))
    f.flat_statements.append(ir.AddressOf(ptr_dst, dst))

    fn_copy = tc.resolve_function("__copy__", [], [ts.PointerType(f.types[dst]), ts.PointerType(f.types[src])])
    add_func_call(
            sa_node,
            f, 
            tc, 
            fn_copy, 
            [ptr_dst, ptr_src], 
            [False, False], 
            "copy_call"
    )

# structural

@add_method_te_visit(sa.Program)
def _(self: sa.Program, tc: TC):
    raise RuntimeError(f"this is not parsed directly")


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
    sms = tc.scope_man.get_size()
    tc.scope_man.begin_scope()

    try:
        def infer_ret_type():
            try:
                retty = self.expr_ret.te_visit(tc, f)
            except ierr.InferenceError as e:
                raise ierr.TypeExpressionError(f"Can not infer return type at {self.linespan[0]}") from e

            tc.function_type_container[desc] = f
            f.types["return"] = retty
            if retty != ts.VoidType():
                f.flat_statements.append(ir.StackAllocate("return"))

        f = ts.FunctionTypeNormal(self.name)
        f.mangled_name = tc.scope_man.new_func_name(self.name)

        # type params
        for name, t in zip(self.type_parameter_names, type_args_types):
            n = tc.scope_man.new_var_name(name, type_name=True)
            f.types[n] = t

        # params
        for name, t in zip(self.parameter_names, args_types):
            n = new_stack_symbolic_register(self, f, tc, t, name)

            pp = "param_placeholder"+n
            f.parameter_names_ordered.append(pp)
            f.types[pp] = t

            f.flat_statements.append(ir.StackStore(n, pp))
            if f.dest_params:
                tc.scope_man.add_to_dest(n)


        f.flat_statements.append(ir.Comment("func setup done"))

        for s in self.statement_list:
            if not "return" in f.types and not isinstance(s, sa.TypeDeclarationStatementFunction):
                infer_ret_type()

            s.te_visit(tc, f)

        if not "return" in f.types:
            infer_ret_type()

        # destruct and return
        f.flat_statements.append(ir.JumpToLabel("func_end"))
        f.flat_statements.append(ir.Label("func_end"))

        for td in tc.scope_man.get_dest_list():
            add_dest(self, f, tc, td)
        f.flat_statements.append(ir.FunctionReturn())

        tc.scope_man.end_scope()
        return f

    except ierr.InferenceError as e:
        tc.scope_man.clear(sms)
        if desc in tc.function_type_container:
            tc.function_type_container.pop(desc)
        raise ierr.InferenceError(f"Can not synthetize function at {self.linespan[0]}") from e


@add_method_te_visit(sa.StructDefinition)
def _(self: sa.StructDefinition, tc: TC,
      type_args: List[ts.Type],
      ):
    s = ts.StructType(self.name)

    s.types = dict([
        a for a in zip(self.type_parameter_names, type_args)
    ])

    for stat in self.statement_list:
        stat.te_visit(tc, s)

    if s.return_type is not None and len(s.members)>0:
        raise ierr.InferenceError(f"Can't have both return types and members in a struct, at {self.linespan[0]}") from e

    if s.return_type is not None:
        return s.return_type
    else:
        s.mangled_name = tc.scope_man.new_struct_name(self.name)
        return s


# function statements

@add_method_te_visit(sa.BlockStatement)
def _(self: sa.BlockStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    tc.scope_man.begin_scope()
    for s in self.statement_list:
        self.expr.te_visit(tc, f)

    for td in tc.scope_man.get_dest_list():
        add_dest(self, f,tc,td)
    tc.scope_man.end_scope()


@add_method_te_visit(sa.ExpressionStatement)
def _(self: sa.ExpressionStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    e = self.expr.te_visit(tc, f)
    if e is not None and not self.expr.lvalue:
        add_dest(self, f, tc, e)


@add_method_te_visit(sa.TypeDeclarationStatementFunction)
def _(self: sa.TypeDeclarationStatementFunction, tc: TC,
        f: ts.FunctionTypeNormal):
    mn = tc.scope_man.new_var_name(self.name, type_name=True)
    f.types[mn] = self.type_expr.te_visit(tc, f)


@add_method_te_visit(sa.AssignmentStatement)
def _(self: sa.AssignmentStatement, tc: TC,
        f: ts.FunctionTypeNormal):

    le = self.left.te_visit(tc, f)
    if not self.left.lvalue:
        raise ierr.RuntimeExpressionError(f"Require lvalue at {self.linespan[0]}!")

    re = self.right.te_visit(tc, f)

    if f.types[le] != f.types[re]:
        raise ierr.RuntimeExpressionError(f"type missmatch at {self.linespan[0]}")
    else:
        # destroy left side
        add_dest(self, f, tc, le)

        # copy or memory copy
        if self.right.lvalue:
            add_copy(self, f, tc, le, re)
        else:
            f.flat_statements.append(ir.StackCopy(le, re))


@add_method_te_visit(sa.InitStatement)
def _(self: sa.InitStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    e = self.expr.te_visit(tc, f)

    mn = new_stack_symbolic_register(self, f, tc, f.types[e], self.name)
    tc.scope_man.add_to_dest(mn)


    if self.expr.lvalue:
        add_copy(self, f, tc, mn, e)
    else:
        f.flat_statements.append(ir.StackCopy(mn, e))


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
        raise ierr.RuntimeExpressionError(f"check expr must be bool, at {self.expr_check.lineno[0]}")

    f.flat_statements.append(ir.Label(lwc))
    f.flat_statements.append(ir.JumpToLabelConditional(ec, lws, lwe))
    f.flat_statements.append(ir.Label(lws))
    for s in self.statement_list:
        s.te_visit(tc, f) 

    f.flat_statements.append(ir.Label(lwe))
    if not self.expr_check.lvalue:
        add_dest(self, f, tc, ec)

    
    for td in tc.scope_man.get_dest_list():
        add_dest(self, f,tc,td)
    tc.scope_man.end_scope()
    f.break_label_stack.pop()


@add_method_te_visit(sa.ForStatement)
def _(self: sa.ForStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    lfcheck = tc.scope_man.new_label_name("for_check")
    lfsucc = tc.scope_man.new_label_name("for_succ")
    lfchange = tc.scope_man.new_label_name("for_change")
    lfe = tc.scope_man.new_label_name("for_end")
    f.break_label_stack.append(lfe)

    tc.scope_man.begin_scope()

    self.stat_init.te_visit(tc, f)

    f.flat_statements.append(ir.JumpToLabel(lfcheck))
    f.flat_statements.append(ir.Label(lfcheck))

    ec = self.expr_check.te_visit(tc, f)

    if not isinstance(f.types[ec], ts.BoolType):
        raise ierr.RuntimeError(f"check expr must be bool, at {self.expr_check.lineno[0]}")

    f.flat_statements.append(ir.JumpToLabelConditional(ec, lfsucc, lfe))
    f.flat_statements.append(ir.Label(lfsucc))
    for s in self.statement_list:
        s.te_visit(tc, f)

    f.flat_statements.append(ir.JumpToLabel(lfchange))
    f.flat_statements.append(ir.Label(lfchange))
    self.stat_change.te_visit(tc, f)

    f.flat_statements.append(ir.JumpToLabel(lfcheck))

    f.flat_statements.append(ir.Label(lfe))
    if not self.expr_check.lvalue:
        add_dest(self, f, tc, ec)

    for td in tc.scope_man.get_dest_list():
        add_dest(self, f,tc,td)

    tc.scope_man.end_scope()
    f.break_label_stack.pop()


@add_method_te_visit(sa.IfElseStatement)
def _(self: sa.IfElseStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    iftrue = tc.scope_man.new_label_name("if_true")
    iffalse = tc.scope_man.new_label_name("if_false")
    ifend = tc.scope_man.new_label_name("if_end")

    tc.scope_man.begin_scope()
    ec = self.expr_check.te_visit(tc, f)

    if not isinstance(f.types[ec], ts.BoolType):
        raise ierr.RuntimeError(f"check expr must be bool\
                at {self.expr_check.lineno[0]}") 

    f.flat_statements.append(ir.JumpToLabelConditional(ec, iftrue, iffalse))
    f.flat_statements.append(ir.Label(iftrue))
    for s in self.statement_list_true:
        s.te_visit(tc, f)
    f.flat_statements.append(ir.JumpToLabel(ifend))

    f.flat_statements.append(ir.Label(iffalse))
    for s in self.statement_list_false:
        s.te_visit(tc, f)

    f.flat_statements.append(ir.Label(ifend))
    if not self.expr_check.lvalue:
        add_dest(self, f, tc, ec)

    for td in tc.scope_man.get_dest_list():
        add_dest(self, f,tc,td)
    tc.scope_man.end_scope()


@add_method_te_visit(sa.ReturnStatement)
def _(self: sa.ReturnStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    if self.expr is None:
        if f.types["return"]!=ts.VoidType():
            raise ierr.InferenceError(f"type missmatch with return {self.linespan[0]}")
        f.flat_statements.append(ir.JumpToLabel("func_end"))
    else:
        e = self.expr.te_visit(tc, f)

        if f.types[e] != f.types["return"]:
            raise ierr.InferenceError(f"type missmatch with return {self.linespan[0]}")

        f.flat_statements.append(ir.StackCopy("return", e))
        f.flat_statements.append(ir.JumpToLabel("func_end"))


@add_method_te_visit(sa.BreakStatement)
def _(self: sa.BreakStatement, tc: TC,
        f: ts.FunctionTypeNormal):
    if self.no <= 0:
        raise ierr.RuntimeExpressionError(f"break must be >0")
    if self.no > len(f.break_label_stack):
        raise ierr.RuntimeExpressionError(f"dont have enough \
                loops to break out of")

    f.flat_statements.append(ir.JumpToLabel(
        f.break_label_stack[len(f.break_label_stack)-self.no]
    ))


# struct statements


@add_method_te_visit(sa.MemberDeclarationStatement)
def _(self: sa.MemberDeclarationStatement, tc: TC,
        s: ts.StructType):
    if s.return_type is not None:
        raise ierr.TypeExpressionError(f"statement after return in struct, at {self.linespan[0]}")
    t = self.type_expr.te_visit(tc, s)
    if self.name in s.types:
        raise ierr.TypeExpressionError(f"redefinition of name {self.name}")

    s.types[self.name] = t
    s.members.append(self.name)

@add_method_te_visit(sa.TypeReturnStatement)
def _(self: sa.TypeReturnStatement, tc: TC,
        s: ts.StructType):
    t = self.type_expr.te_visit(tc, s)
    if s.return_type is not None:
        raise ierr.TypeExpressionError(f"multiple returns in struct, at {self.linespan[0]}")
    s.return_type = t


@add_method_te_visit(sa.TypeDeclarationStatementStruct)
def _(self: sa.TypeDeclarationStatementStruct, tc: TC,
        s: ts.StructType):
    if s.return_type is not None:
        raise ierr.TypeExpressionError(f"statement after return in struct, at {self.linespan[0]}")
    t = self.type_expr.te_visit(tc, s)
    if self.name in s.types:
        raise ierr.TypeExpressionError(f"redefinition of name {self.name}")
    s.types[self.name] = t


# value expressions

@add_method_te_visit(sa.IdExpression)
def _(self: sa.IdExpression, tc: TC,
        f: ts.FunctionTypeNormal):
    self.lvalue = True
    tmp = get_stack_symbolic_register(self, f, tc, self.name)
    return tmp


@add_method_te_visit(sa.BracketCallExpression)
def _(self: sa.BracketCallExpression, tc: TC,
        f: ts.FunctionTypeNormal):
    e = self.expr.te_visit(tc, f)
    if not isinstance(f.types[e], ts.PointerType):
        raise ierr.RuntimeExpressionError(f"Can not offset a non-pointer type, at {self.linespan[0]}!")

    ind = self.index.te_visit(tc, f)
    if ind is None: return None
    if not isinstance(f.types[ind], ts.IntType):
        raise ierr.RuntimeExpressionError(f"Can not offset with a non-int type, at {self.linespan[0]}!")

    self.lvalue = self.expr.lvalue

    tmp = new_tmp_stack_symbolic_register(f, tc, f.types[e], "bracket_call")
    f.flat_statements.append(ir.GetPointerOffset(tmp, e, ind, f.types[ind].size))

    return tmp


@add_method_te_visit(sa.MemberIndexExpression)
def _(self: sa.MemberIndexExpression, tc: TC,
        f: ts.FunctionTypeNormal):
    e = self.expr.te_visit(tc, f)

    if not isinstance(f.types[e], ts.StructType):
        raise ierr.RuntimeExpressionError(f"Can not index a non-struct type, at {self.linespan[0]}!")

    if self.member not in f.types[e].members:
        raise ierr.RuntimeExpressionError(f"Can not index a non-existant struct member {self.member}, at {self.linespan[0]}!")

    self.lvalue = self.expr.lvalue

    tmp = new_tmp_stack_symbolic_register_unallocated(f, tc, f.types[e].types[self.member], "member_index")
    f.flat_statements.append(ir.GetElementPtr(tmp, e, self.member))

    return tmp


@add_method_te_visit(sa.DerefExpression)
def _(self: sa.DerefExpression, tc: TC,
        f: ts.FunctionTypeNormal):
    e = self.expr.te_visit(tc, f)

    if not isinstance(f.types[e], ts.PointerType):
        raise ierr.RuntimeExpressionError(f"Can not dereference a non-pointer type, at {self.linespan[0]}!")

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
        raise ierr.RuntimeExpressionError(f"Taking address requires a lvalue, at {self.linespan[0]}!")

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

    arg_names = [v.te_visit(tc, f) for v in self.args]

    args_types = [f.types[a] for a in arg_names]

    func_call = tc.resolve_function(self.name, type_args_types, args_types)
    copy_bools = [t.lvalue for t in self.args]

    if func_call is not None:
        ret = add_func_call(self, f, tc, func_call, arg_names, copy_bools, "call")
        return ret
    else:
        struct = tc.resolve_struct(self.name, type_args_types)
        init_call = tc.resolve_function("__init__", [], [ts.PointerType(st)]+args_types)

        newo = new_tmp_stack_symbolic_register(f, tc, struct, "newo")
        newo_ptr = new_tmp_stack_symbolic_register(f, tc, ts.PointerType(struct), "ptr_to_newo")
        f.flat_statements.append(ir.AddressOf(newo_ptr, newo))

        add_func_call(self, f, tc, init_call, [newo_ptr]+arg_names, [False]+copy_bools, "init_call")

        st.needs_gen = True
        return reg


# type expressions

@add_method_te_visit(sa.TypeBinaryExpression)
def _(self: sa.TypeBinaryExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

    le = self.left.te_visit(tc, sf)
    re = self.right.te_visit(tc, sf)
    rt = tc.resolve_struct(self.op, [le, re])

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

    if self.name == "enable_if":
        if len(self.expr_list) != 1:
            raise ierr.TypeExpressionError(f"Enable_if has to have 1 expression only")
        else:
            try:
                t_expr = self.expr_list[0].te_visit(tc, sf)
            except ierr.InferenceError:
                raise ierr.ChoiceSkipError(f"Failed enable_if: error, skipping")
            if t_expr != ts.IntType(1):
                raise ierr.ChoiceSkipError(f"Failed enable_if: expr is not true(i1), skipping")
            return t_expr
    else:
        texprs = [te.te_visit(tc, sf) for te in self.expr_list]
        rt = tc.resolve_struct(self.name, texprs)

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
    return rt

@add_method_te_visit(sa.TypeTypeExpression)
def _(self: sa.TypeTypeExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):
    return self.type_obj

@add_method_te_visit(sa.TypeDerefExpression)
def _(self: sa.TypeDerefExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

    e = self.expr.te_visit(tc, sf)

    if isinstance(e, ts.PointerType):
        return e.pointed
    else:
        raise ierr.TypeExpressionError(f"Can not dereference a non-pointer type!")


@add_method_te_visit(sa.TypePtrExpression)
def _(self: sa.TypePtrExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

    e = self.expr.te_visit(tc, sf)

    return ts.PointerType(e)


@add_method_te_visit(sa.TypeIndexExpression)
def _(self: sa.TypeIndexExpression, tc: TC,
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

    e = self.expr.te_visit(tc, sf)

    if not isinstance(e, ts.StructType):
        raise ierr.TypeExpressionError(f"Type indexing expression must be done on a struct type!")
    return e.types[self.name]

