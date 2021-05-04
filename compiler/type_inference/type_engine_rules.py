from typing import List, Union, Any

from . import flat_ir as ir
from ..helpers import add_method_te_visit
from ..semantics_parsing import semantic_ast as sa

from . import type_system as ts
from . import inference_errors as ierr
from . import context

# utils for type_engine_rules

def get_func_call(sa_node, 
        fc: context.FunctionContext, 
        tc: context.TypingContext, 
        fn_to_call: ts.FunctionType, 
        args_names: List[str], 
        args_lvalues: List[bool]):
    """
    Copies the arguments beforehand, if needed
    (needed combines the logic of lvalues and overriding with no copy)

    RETURNS a new stack symbolic register or None
    """

    types = [fc.types[n] for n in args_names] 

    copied_args_names = []
    for i in range(len(args_names)):
        if not args_lvalues[i] or fn_to_call.do_not_copy_args:
            copied_args_names.append(args_names[i])
        else:
            copy_reg = ir.get_stack_allocate_tmp(f"copied_arg_{i}", types[i], fc)
            put_copy(sa_node, fc, tc, copy_reg, args_names[i])
            copied_args_names.append(copy_reg)

    return ir.function_call(ret_reg, fn_to_call, copied_args_names)

def put_dest(sa_node, 
        fc: context.FunctionContext, 
        tc: context.TypingContext, 
        name: str):
    """
    Expects a stack symbolic registers with type s.
    """

    ptr_name = ir.get_address_of(name, fc)

    pt = ts.PointerType(fc.types[name])

    fn_dest = tc.resolve_function("__dest__", (), (pt))
    get_func_call(
            sa_node,
            fc, 
            tc, 
            fn_dest, 
            [ptr_name], 
            [False], 
    )

def put_copy(sa_node, 
        fc: context.FunctionContext, 
        tc: context.TypingContext, 
        dst: str, 
        src: str):
    """
    Expects two stack symbolic registers with type s.
    """

    ptr_src = ir.get_address_of(src, fc)
    ptr_dst = ir.get_address_of(dst, fc)

    pt = ts.PointerType(fc.types[src])

    fn_copy = tc.resolve_function("__copy__", (), (pt, pt))
    get_func_call(
            sa_node,
            f, 
            tc, 
            fn_copy, 
            [ptr_dst, ptr_src], 
            [False, False], 
    )

# structural

@add_method_te_visit(sa.FunctionDefinition)
def _(self: sa.FunctionDefinition, tc: context.TypingContext,
      type_args_types: Tuple[ts.Type],
      args_types: Tuple[ts.Type],
      ) -> Any:
    desc = (
        self.name,
        type_args_types,
        args_types
    )
    try:
        mn = tc.scope_man.new_func_name(self.name)
        fc = context.FunctionContext(mn)
        fc.scope_man.begin_scope()

        def infer_ret_type():
            try:
                retty = self.expr_ret.te_visit(tc, f)
            except ierr.InferenceError as e:
                raise ierr.TypeExpressionError(f"Can not infer return type at {self.linespan[0]}") from e

            fc.return_type = retty
            if retty != ts.VoidType():
                ir.stack_allocate("return", retty, fc)

            # this is crucial for recursive calls
            tc.function_type_container[desc] = ts.FunctionType(
                    mn,
                    retty,
                    default = False,
                    do_not_copy_args = True,
                    code = None
            )

        # type params
        for name, ty in zip(self.type_parameter_names, type_args_types):
            n = fc.scope_man.new_var_name(name, type_name=True)
            fc.types[n] = ty

        # params
        for name, ty in zip(self.parameter_names, args_types):
            ir.param_to_stack_store(name, ty, fc))

        ir.comment("func setup done", fc)

        # statements
        for s in self.statement_list:
            if fc.return_type is None and not isinstance(s, sa.TypeDeclarationStatementFunction):
                infer_ret_type()
            s.te_visit(tc, fc)

        if fc.return_type is None:
            infer_ret_type()

        # destruct and return
        ir.jump_to_label("func_end", fc)
        ir.label("func_end",fc)

        for td in tc.scope_man.get_dest_list():
            add_dest(self, f, tc, td)
        ir.function_return(fc)

        # cleanup
        fc.scope_man.end_scope()
        return ts.FunctionType(fc.mangled_name, fc.return_type, default=False, do_not_copy_args=False, code=fc.code) 

    except ierr.InferenceError as e:
        raise ierr.InferenceError(f"Can not synthetize function at {self.linespan[0]}") from e

    finally:
        # recursive calls cleanup
        if desc in tc.function_type_container:
            tc.function_type_container.pop(desc)


@add_method_te_visit(sa.StructDefinition)
def _(self: sa.StructDefinition, tc: context.TypingContext,
      type_args: List[ts.Type],
      ):
    mn = tc.scope_man.new_struct_name(self.name)
    sc = context.StructContext(mn)

    sc.types = dict([
        a for a in zip(self.type_parameter_names, type_args)
    ])

    for stat in self.statement_list:
        stat.te_visit(tc, sc)

    if self.return_type_expr is not None and len(s.members)>0:
        raise ierr.InferenceError(f"Can not have both return type and members in a struct, at {self.linespan[0]}") from e

    if s.return_type is not None:
        rt = self.return_type_expr.te_visit(tc, sc)
        return rt
    else:
        return ts.StructType(sc.mangled_name, sc.types, sc.members, sc.return_type)


# function statements

@add_method_te_visit(sa.BlockStatement)
def _(self: sa.BlockStatement, tc: context.TypingContext,
        fc: context.FunctionContext):
    fc.scope_man.begin_scope()
    fc.dest_stack.append([])

    for s in self.statement_list:
        self.expr.te_visit(tc, fc)

    for td in fc.dest_stack[-1]:
        put_dest(self, fc, tc, td)
    fc.dest_stack.pop()
    fc.scope_man.end_scope()


@add_method_te_visit(sa.ExpressionStatement)
def _(self: sa.ExpressionStatement, tc: context.TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, f)
    if e is not None and not self.expr.lvalue:
        add_dest(self, f, tc, e)


@add_method_te_visit(sa.TypeDeclarationStatementFunction)
def _(self: sa.TypeDeclarationStatementFunction, tc: context.TypingContext,
        f: ts.FunctionTypeNormal):
        fc: context.FunctionContext):
    mn = tc.scope_man.new_var_name(self.name, type_name=True)
    f.types[mn] = self.type_expr.te_visit(tc, f)


@add_method_te_visit(sa.AssignmentStatement)
def _(self: sa.AssignmentStatement, tc: context.TypingContext,
        f: ts.FunctionTypeNormal):
        fc: context.FunctionContext):

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
            fc.flat_statements.extend(ir.StackCopy(le, re))


@add_method_te_visit(sa.InitStatement)
def _(self: sa.InitStatement, tc: context.TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, fc)
    mn = tc.scope_man.new_var_name(self.name)
    fc.dest_stack[-1].append(mn)

    if mn is None:
        raise ierr.RuntimeExpressionError(f"Name duplication ({name}), at {sa_node.linespan[0]}!")

    ir.put_stack_allocate(mn, fc.types[e], fc)
    if self.expr.lvalue:
        add_copy(self, f, tc, mn, e)
    else:
        ir.put_stack_copy(mn, e, fc)


@add_method_te_visit(sa.WhileStatement)
def _(self: sa.WhileStatement, tc: context.TypingContext,
        f: ts.FunctionTypeNormal):
        fc: context.FunctionContext):
    lwc = tc.scope_man.new_label_name("while check")
    lws = tc.scope_man.new_label_name("while succ")
    lwe = tc.scope_man.new_label_name("while end")
    f.break_label_stack.append(lwe)

    tc.scope_man.begin_scope()

    ec = self.expr_check.te_visit(tc, f)
    if ec is None or not isinstance(f.types[ec],ts.BoolType):
        raise ierr.RuntimeExpressionError(f"check expr must be bool, at {self.expr_check.lineno[0]}")

    fc.flat_statements.extend(ir.Label(lwc))
    fc.flat_statements.extend(ir.JumpToLabelConditional(ec, lws, lwe))
    fc.flat_statements.extend(ir.Label(lws))
    for s in self.statement_list:
        s.te_visit(tc, f) 

    fc.flat_statements.extend(ir.Label(lwe))
    if not self.expr_check.lvalue:
        add_dest(self, f, tc, ec)

    
    for td in tc.scope_man.get_dest_list():
        add_dest(self, f,tc,td)
    tc.scope_man.end_scope()
    f.break_label_stack.pop()


@add_method_te_visit(sa.ForStatement)
def _(self: sa.ForStatement, tc: context.TypingContext,
        f: ts.FunctionTypeNormal):
        fc: context.FunctionContext):
    lfcheck = tc.scope_man.new_label_name("for_check")
    lfsucc = tc.scope_man.new_label_name("for_succ")
    lfchange = tc.scope_man.new_label_name("for_change")
    lfe = tc.scope_man.new_label_name("for_end")
    f.break_label_stack.append(lfe)

    tc.scope_man.begin_scope()

    self.stat_init.te_visit(tc, f)

    fc.flat_statements.extend(ir.JumpToLabel(lfcheck))
    fc.flat_statements.extend(ir.Label(lfcheck))

    ec = self.expr_check.te_visit(tc, f)

    if not isinstance(f.types[ec], ts.BoolType):
        raise ierr.RuntimeError(f"check expr must be bool, at {self.expr_check.lineno[0]}")

    fc.flat_statements.extend(ir.JumpToLabelConditional(ec, lfsucc, lfe))
    fc.flat_statements.extend(ir.Label(lfsucc))
    for s in self.statement_list:
        s.te_visit(tc, f)

    fc.flat_statements.extend(ir.JumpToLabel(lfchange))
    fc.flat_statements.extend(ir.Label(lfchange))
    self.stat_change.te_visit(tc, f)

    fc.flat_statements.extend(ir.JumpToLabel(lfcheck))

    fc.flat_statements.extend(ir.Label(lfe))
    if not self.expr_check.lvalue:
        add_dest(self, f, tc, ec)

    for td in tc.scope_man.get_dest_list():
        add_dest(self, f,tc,td)

    tc.scope_man.end_scope()
    f.break_label_stack.pop()


@add_method_te_visit(sa.IfElseStatement)
def _(self: sa.IfElseStatement, tc: context.TypingContext,
        fc: context.FunctionContext):
    iftrue = tc.scope_man.new_label_name("if_true")
    iffalse = tc.scope_man.new_label_name("if_false")
    ifend = tc.scope_man.new_label_name("if_end")

    tc.scope_man.begin_scope()
    ec = self.expr_check.te_visit(tc, f)

    if not isinstance(f.types[ec], ts.BoolType):
        raise ierr.RuntimeError(f"check expr must be bool\
                at {self.expr_check.lineno[0]}") 

    fc.flat_statements.extend(ir.JumpToLabelConditional(ec, iftrue, iffalse))
    fc.flat_statements.extend(ir.Label(iftrue))
    for s in self.statement_list_true:
        s.te_visit(tc, f)
    fc.flat_statements.extend(ir.JumpToLabel(ifend))

    fc.flat_statements.extend(ir.Label(iffalse))
    for s in self.statement_list_false:
        s.te_visit(tc, f)

    fc.flat_statements.extend(ir.Label(ifend))
    if not self.expr_check.lvalue:
        add_dest(self, f, tc, ec)

    for td in tc.scope_man.get_dest_list():
        add_dest(self, f,tc,td)
    tc.scope_man.end_scope()


@add_method_te_visit(sa.ReturnStatement)
def _(self: sa.ReturnStatement, tc: context.TypingContext,
        fc: context.FunctionContext):
    if self.expr is None:
        if f.types["return"]!=ts.VoidType():
            raise ierr.InferenceError(f"type missmatch with return {self.linespan[0]}")
        fc.flat_statements.extend(ir.JumpToLabel("func_end"))
    else:
        e = self.expr.te_visit(tc, f)

        if f.types[e] != f.types["return"]:
            raise ierr.InferenceError(f"type missmatch with return {self.linespan[0]}")

        fc.flat_statements.extend(ir.StackCopy("return", e))
        fc.flat_statements.extend(ir.JumpToLabel("func_end"))


@add_method_te_visit(sa.BreakStatement)
def _(self: sa.BreakStatement, tc: context.TypingContext,
        fc: context.FunctionContext):
    if self.no <= 0:
        raise ierr.RuntimeExpressionError(f"break must be >0")
    if self.no > len(f.break_label_stack):
        raise ierr.RuntimeExpressionError(f"dont have enough \
                loops to break out of")

    fc.flat_statements.extend(ir.JumpToLabel(
        f.break_label_stack[len(f.break_label_stack)-self.no]
    ))


# struct statements


@add_method_te_visit(sa.MemberDeclarationStatement)
def _(self: sa.MemberDeclarationStatement, tc: context.TypingContext,
        s: ts.StructType):
    if s.return_type is not None:
        raise ierr.TypeExpressionError(f"statement after return in struct, at {self.linespan[0]}")
    t = self.type_expr.te_visit(tc, s)
    if self.name in s.types:
        raise ierr.TypeExpressionError(f"redefinition of name {self.name}")

    s.types[self.name] = t
    s.members.append(self.name)

@add_method_te_visit(sa.TypeDeclarationStatementStruct)
def _(self: sa.TypeDeclarationStatementStruct, tc: context.TypingContext,
        s: ts.StructType):
    if s.return_type is not None:
        raise ierr.TypeExpressionError(f"statement after return in struct, at {self.linespan[0]}")
    t = self.type_expr.te_visit(tc, s)
    if self.name in s.types:
        raise ierr.TypeExpressionError(f"redefinition of name {self.name}")
    s.types[self.name] = t


# value expressions

@add_method_te_visit(sa.IdExpression)
def _(self: sa.IdExpression, tc: context.TypingContext,
        fc: context.FunctionContext):
    mn = tc.scope_man.get_var_name(name)
    self.lvalue = True

    if mn is None:
        raise ierr.RuntimeExpressionError(f"Variable {name} not defined, at {sa_node.linespan[0]}!")

    return tmp


@add_method_te_visit(sa.BracketCallExpression)
def _(self: sa.BracketCallExpression, tc: context.TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, f)
    ind = self.index.te_visit(tc, f)
    self.lvalue = self.expr.lvalue

    if not isinstance(f.types[e], ts.PointerType):
        raise ierr.RuntimeExpressionError(f"Can not offset a non-pointer type, at {self.linespan[0]}!")

    if not isinstance(f.types[ind], ts.IntType):
        raise ierr.RuntimeExpressionError(f"Can not offset with a non-int type, at {self.linespan[0]}!")


    return ir.get_pointer_offset(e, ind, fc)


#1
@add_method_te_visit(sa.MemberIndexExpression)
def _(self: sa.MemberIndexExpression, tc: context.TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, f)
    self.lvalue = self.expr.lvalue

    if not isinstance(fc.types[e], ts.StructType):
        raise ierr.RuntimeExpressionError(f"Can not index a non-struct type, at {self.linespan[0]}!")

    if self.member not in fc.types[e].members:
        raise ierr.RuntimeExpressionError(f"Can not index a non-existant struct member {self.member}, at {self.linespan[0]}!")


    return ir.get_member(e, self.member, fc)


@add_method_te_visit(sa.DerefExpression)
def _(self: sa.DerefExpression, tc: context.TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, f)
    self.lvalue = self.expr.lvalue

    if not isinstance(f.types[e], ts.PointerType):
        raise ierr.RuntimeExpressionError(f"Can not dereference a non-pointer type, at {self.linespan[0]}!")

    return ir.get_dereference(e, fc)


@add_method_te_visit(sa.AddressExpression)
def _(self: sa.BinaryExpression, tc: context.TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, f)
    self.lvalue = False

    if not self.expr.lvalue:
        raise ierr.RuntimeExpressionError(f"Taking address requires a lvalue, at {self.linespan[0]}!")

    tmp = new_tmp_stack_symbolic_register(f, tc, ts.PointerType(f.types[e]), "addrof")
    fc.flat_statements.extend(ir.AddressOf(tmp, e))

    return tmp


@add_method_te_visit(sa.IntLiteralExpression)
def _(self: sa.IntLiteralExpression, tc: context.TypingContext,
        fc: context.FunctionContext):
    self.lvalue = False

    tmp = new_tmp_stack_symbolic_register(f, tc, ts.IntType(self.size), "int_lit")
    fc.flat_statements.extend(ir.IntConstantAssignment(tmp,
                                                      self.value,
                                                      self.size))
    return tmp


@add_method_te_visit(sa.BoolLiteralExpression)
def _(self: sa.BoolLiteralExpression, tc: context.TypingContext,
        fc: context.FunctionContext):
    self.lvalue = False

    tmp = new_tmp_stack_symbolic_register(f, tc, ts.BoolType(), "bool_lit")
    fc.flat_statements.extend(ir.BoolConstantAssignment(tmp,
                                                       self.value))
    return tmp


@add_method_te_visit(sa.CallExpression)
def _(self: sa.CallExpression, tc: context.TypingContext,
        fc: context.FunctionContext):
    self.lvalue = False

    type_args_types = [t.te_visit(tc, f) for t in self.type_expr_list]

    arg_names = [v.te_visit(tc, f) for v in self.args]
    args_types = [f.types[a] for a in arg_names]
    copy_bools = [t.lvalue for t in self.args]

    try:
        func_call = tc.resolve_function(self.name, tuple(type_args_types), tuple(args_types))
    except ierr.InferenceError as e:
        raise ierr.InferenceError(f"Can not infer function call at {self.linespan[0]}") from e

    ret = get_func_call(self, f, tc, func_call, arg_names, copy_bools, "call")
    return ret


# type expressions

@add_method_te_visit(sa.TypeBinaryExpression)
def _(self: sa.TypeBinaryExpression, tc: context.TypingContext,
        sfc: Union[context.StructContext, context.FunctionContext]):

    le = self.left.te_visit(tc, sfc)
    re = self.right.te_visit(tc, sfc)
    rt = tc.resolve_struct(self.op, [le, re])

    return rt


@add_method_te_visit(sa.TypeAngleExpression)
def _(self: sa.TypeAngleExpression, tc: context.TypingContext,
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
            t_expr = self.expr_list[0].te_visit(tc, sf)
            if t_expr != ts.IntType(1):
                raise ierr.ChoiceSkipError(f"Failed enable_if: expr is not true(i1), skipping at {self.linespan[0]}")
            return t_expr
    if self.name == "enable_if_resolve":
        if len(self.expr_list) != 1:
            raise ierr.TypeExpressionError(f"Enable_if_resolve has to have 1 expression only")
        else:
            try:
                t_expr = self.expr_list[0].te_visit(tc, sf)
            except ierr.InferenceError as e:
                raise ierr.ChoiceSkipError(f"Failed enable_if_resolve: error at resolution, skipping at {self.linespan[0]}") from e
            return t_expr
    else:
        texprs = [te.te_visit(tc, sf) for te in self.expr_list]
        rt = tc.resolve_struct(self.name, texprs)

        return rt

@add_method_te_visit(sa.TypeIdExpression)
def _(self: sa.TypeIdExpression, tc: context.TypingContext,
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
def _(self: sa.TypeTypeExpression, tc: context.TypingContext,
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):
    return self.type_obj

@add_method_te_visit(sa.TypeDerefExpression)
def _(self: sa.TypeDerefExpression, tc: context.TypingContext,
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

    e = self.expr.te_visit(tc, sf)

    if isinstance(e, ts.PointerType):
        return e.pointed
    else:
        raise ierr.TypeExpressionError(f"Can not dereference a non-pointer type!")


@add_method_te_visit(sa.TypePtrExpression)
def _(self: sa.TypePtrExpression, tc: context.TypingContext,
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

    e = self.expr.te_visit(tc, sf)

    return ts.PointerType(e)


@add_method_te_visit(sa.TypeIndexExpression)
def _(self: sa.TypeIndexExpression, tc: context.TypingContext,
        sf: Union[ts.StructType, ts.FunctionTypeNormal]):

    e = self.expr.te_visit(tc, sf)

    if not isinstance(e, ts.StructType):
        raise ierr.TypeExpressionError(f"Type indexing expression must be done on a struct type!")
    return e.types[self.name]

