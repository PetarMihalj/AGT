from typing import List, Union, Any, Tuple

from . import flat_ir as ir
from ..semantics_parsing import semantic_ast as sa

from . import type_system as ts
from . import inference_errors as ierr
from . import context
from . import code_blocks
from .type_engine import TypingContext

# utils for type_engine_rules

def get_func_call(sa_node, 
        fc: context.FunctionContext, 
        tc: TypingContext, 
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

    return ir.get_function_call(fn_to_call, copied_args_names, fc)

def put_dest(sa_node, 
        fc: context.FunctionContext, 
        tc: TypingContext, 
        name: str):
    """
    Expects a stack symbolic registers with type s.
    """

    ptr_name = ir.get_address_of(name, fc)

    pt = ts.PointerType(fc.types[name])

    fn_dest = tc.resolve_function("__dest__", (), (pt,))
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
        tc: TypingContext, 
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
            fc, 
            tc, 
            fn_copy, 
            [ptr_dst, ptr_src], 
            [False, False], 
    )

# structural

def add_method_te_visit(cls):
    def go(func):
        def wrapper(self, *vargs, **kwargs):
            tc = vargs[0]

            a = func(self, *vargs, **kwargs)
            if hasattr(a, "__dict__") and hasattr(self, "linespan"):
                a.linespan = self.linespan
                a.lexspan = self.lexspan
            return a
        setattr(cls, "te_visit", wrapper)
    return go

@add_method_te_visit(sa.FunctionDefinition)
def _(self: sa.FunctionDefinition, tc: TypingContext,
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
        fc.dest_stack.append([])

        did_infer_return = False

        def infer_ret_type():
            try:
                if self.expr_ret is not None:
                    retty = self.expr_ret.te_visit(tc, fc)
                else:
                    retty = None

            except ierr.InferenceError as e:
                raise ierr.TypeExpressionError(f"Can not infer return type at {self.linespan[0]}") from e

            fc.return_type = retty
            if retty is not None:
                ir.put_stack_allocate("return", retty, fc)

            # this is crucial for recursive calls
            tc.function_type_container[desc] = ts.FunctionType(
                    mn,
                    retty,
                    do_not_copy_args = False,
            )

        # type params
        for name, ty in zip(self.type_parameter_names, type_args_types):
            n = fc.scope_man.new_var_name(name, type_name=True)
            fc.types[n] = ty

        # params
        for name, ty in zip(self.parameter_names, args_types):
            ir.put_param_to_stack_store(name, ty, fc)

        ir.put_comment("func setup done", fc)

        # statements
        for s in self.statement_list:
            if not did_infer_return and not isinstance(s, sa.TypeDeclarationStatementFunction):
                infer_ret_type()
                did_infer_return = True
            s.te_visit(tc, fc)

        if not did_infer_return:
            infer_ret_type()
            did_infer_return = True

        # destruct and return
        ir.put_jump_to_label("func_end", fc)
        ir.put_label("func_end",fc)

        for td in fc.dest_stack[-1]:
            put_dest(self, fc, tc, td)
        ir.put_function_return(fc)

        # cleanup
        fc.dest_stack.pop()
        fc.scope_man.end_scope()

        tc.code_blocks.append(code_blocks.FuncTypeCodeBlock(fc))
        return ts.FunctionType(fc.mangled_name, fc.return_type, do_not_copy_args=False) 

    except ierr.CrashingError as e:
        raise ierr.InferenceError(f"Can not synthetize function at {self.linespan[0]}") from e

    finally:
        # recursive calls cleanup
        if desc in tc.function_type_container:
            tc.function_type_container.pop(desc)


@add_method_te_visit(sa.StructDefinition)
def _(self: sa.StructDefinition, tc: TypingContext,
      type_args: List[ts.Type],
      ):
    mn = tc.scope_man.new_struct_name(self.name)
    sc = context.StructContext(mn)

    sc.types = dict([
        a for a in zip(self.type_parameter_names, type_args)
    ])

    for stat in self.statement_list:
        stat.te_visit(tc, sc)

    if self.return_type_expr is not None and len(sc.members)>0:
        raise ierr.InferenceError(f"Can not have both return type and members in a struct, at {self.linespan[0]}") from e

    if self.return_type_expr is not None:
        sc.return_type = self.return_type_expr.te_visit(tc, sc)

    tc.code_blocks.append(code_blocks.StructTypeCodeBlock(sc))
    if sc.return_type is not None:
        rt = self.return_type_expr.te_visit(tc, sc)
        return rt
    else:
        return ts.StructType(sc.mangled_name, sc.types, sc.members, sc.return_type)


# function statements

@add_method_te_visit(sa.BlockStatement)
def _(self: sa.BlockStatement, tc: TypingContext,
        fc: context.FunctionContext):
    fc.scope_man.begin_scope()
    fc.dest_stack.append([])

    for s in self.statement_list:
        s.te_visit(tc, fc)

    for td in fc.dest_stack[-1]:
        put_dest(self, fc, tc, td)
    fc.dest_stack.pop()
    fc.scope_man.end_scope()


@add_method_te_visit(sa.ExpressionStatement)
def _(self: sa.ExpressionStatement, tc: TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, fc)

    # None is for the functions which don not return a value
    if e is not None and not self.expr.lvalue:
        put_dest(self, fc, tc, e)


@add_method_te_visit(sa.TypeDeclarationStatementFunction)
def _(self: sa.TypeDeclarationStatementFunction, tc: TypingContext,
        fc: context.FunctionContext):

    e = self.type_expr.te_visit(tc, fc)

    if self.name != '_':
        mn = fc.scope_man.new_var_name(self.name, type_name=True)
        if mn is None:
            raise ierr.RuntimeExpressionError(f"Name duplication ({self.name}), at {sa_node.linespan[0]}!")
        fc.types[mn] = e


@add_method_te_visit(sa.AssignmentStatement)
def _(self: sa.AssignmentStatement, tc: TypingContext,
        fc: context.FunctionContext):

    le = self.left.te_visit(tc, fc)
    if not self.left.lvalue:
        raise ierr.RuntimeExpressionError(f"Require lvalue at {self.linespan[0]}!")

    re = self.right.te_visit(tc, fc)

    if fc.types[le] != fc.types[re]:
        raise ierr.RuntimeExpressionError(f"type missmatch at {self.linespan[0]}")
    else:
        # destroy left side
        put_dest(self, fc, tc, le)

        # copy or memory copy
        if self.right.lvalue:
            put_copy(self, fc, tc, le, re)
        else:
            ir.put_stack_copy(le, re, fc)


@add_method_te_visit(sa.InitStatement)
def _(self: sa.InitStatement, tc: TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, fc)
    mn = fc.scope_man.new_var_name(self.name)
    fc.dest_stack[-1].append(mn)

    if mn is None:
        raise ierr.RuntimeExpressionError(f"Name duplication ({name}), at {sa_node.linespan[0]}!")

    ir.put_stack_allocate(mn, fc.types[e], fc)
    if self.expr.lvalue:
        put_copy(self, fc, tc, mn, e)
    else:
        ir.put_stack_copy(mn, e, fc)


@add_method_te_visit(sa.WhileStatement)
def _(self: sa.WhileStatement, tc: TypingContext,
        fc: context.FunctionContext):
    lwc = fc.scope_man.new_label_name("while_check")
    lws = fc.scope_man.new_label_name("while_succ")
    lwe = fc.scope_man.new_label_name("while_end")

    fc.break_label_stack.append(lwe)
    fc.scope_man.begin_scope()
    fc.dest_stack.append([])

    ir.put_jump_to_label(lwc, fc)
    ir.put_label(lwc, fc)
    ec = self.expr_check.te_visit(tc, fc)
    if not isinstance(fc.types[ec],ts.BoolType):
        raise ierr.RuntimeExpressionError(f"check expr must be bool, at {self.expr_check.lineno[0]}")
    if not self.expr_check.lvalue:
        fc.dest_stack[-1].append(ec)
    ir.put_jump_to_label_conditional(ec, lws, lwe, fc)

    ir.put_label(lws, fc)
    for s in self.statement_list:
        s.te_visit(tc, fc) 
    ir.put_jump_to_label(lwc, fc)

    ir.Label(lwe)
    
    for td in fc.dest_stack[-1]:
        put_dest(self, fc, tc, td)

    fc.dest_stack.pop()
    fc.scope_man.end_scope()
    fc.break_label_stack.pop()


@add_method_te_visit(sa.ForStatement)
def _(self: sa.ForStatement, tc: TypingContext,
        fc: context.FunctionContext):
    lfcheck = fc.scope_man.new_label_name("for_check")
    lfsucc = fc.scope_man.new_label_name("for_succ")
    lfend = fc.scope_man.new_label_name("for_end")

    fc.break_label_stack.append(lfend)
    fc.scope_man.begin_scope()
    fc.dest_stack.append([])

    self.stat_init.te_visit(tc, fc)

    ir.put_jump_to_label(lfcheck, fc)
    ir.put_label(lfcheck, fc)

    ec = self.expr_check.te_visit(tc, fc)
    if not isinstance(fc.types[ec], ts.BoolType):
        raise ierr.RuntimeError(f"check expr must be bool, at {self.expr_check.lineno[0]}")
    if not self.expr_check.lvalue:
        fc.dest_stack[-1].append(ec)
    ir.put_jump_to_label_conditional(ec, lfsucc, lfend, fc)

    ir.put_label(lfsucc, fc)
    for s in self.statement_list:
        s.te_visit(tc, fc)

    self.stat_change.te_visit(tc, fc)
    ir.put_jump_to_label(lfcheck, fc)

    ir.put_label(lfend, fc)

    for td in fc.dest_stack[-1]:
        put_dest(self, fc, tc, td)

    fc.dest_stack.pop()
    fc.scope_man.end_scope()
    fc.break_label_stack.pop()


@add_method_te_visit(sa.IfElseStatement)
def _(self: sa.IfElseStatement, tc: TypingContext,
        fc: context.FunctionContext):
    iftrue = fc.scope_man.new_label_name("if_true")
    iffalse = fc.scope_man.new_label_name("if_false")
    ifend = fc.scope_man.new_label_name("if_end")

    fc.scope_man.begin_scope()
    fc.dest_stack.append([])

    ec = self.expr_check.te_visit(tc, fc)
    if not isinstance(fc.types[ec], ts.BoolType):
        raise ierr.RuntimeError(f"check expr must be bool\
                at {self.expr_check.lineno[0]}") 
    if not self.expr_check.lvalue:
        fc.dest_stack[-1].append(ec)
    ir.put_jump_to_label_conditional(ec, iftrue, iffalse, fc)

    ir.put_label(iftrue, fc)
    for s in self.statement_list_true:
        s.te_visit(tc, fc)
    ir.put_jump_to_label(ifend, fc)

    ir.put_label(iffalse, fc)
    for s in self.statement_list_false:
        s.te_visit(tc, fc)
    ir.put_jump_to_label(ifend, fc)

    ir.put_label(ifend, fc)

    for td in fc.dest_stack[-1]:
        put_dest(self, fc, tc, td)

    fc.dest_stack.pop()
    fc.scope_man.end_scope()


@add_method_te_visit(sa.ReturnStatement)
def _(self: sa.ReturnStatement, tc: TypingContext,
        fc: context.FunctionContext):

    def dest():
        for dest_list in fc.dest_stack[1:]:
            for td in dest_list:
                put_dest(self, fc, tc, td)

    # depending on type
    if self.expr is None:
        if fc.return_type != None:
            raise ierr.InferenceError(f"type missmatch with return at {self.linespan[0]}")
        dest()
        ir.put_jump_to_label("func_end", fc)
    else:
        e = self.expr.te_visit(tc, fc)

        if fc.types[e] != fc.return_type:
            raise ierr.InferenceError(f"type missmatch with return at {self.linespan[0]}")

        ir.put_stack_copy("return", e, fc)
        dest()
        ir.put_jump_to_label("func_end", fc)


@add_method_te_visit(sa.BreakStatement)
def _(self: sa.BreakStatement, tc: TypingContext,
        fc: context.FunctionContext):
    if self.no <= 0:
        raise ierr.RuntimeExpressionError(f"break must be >0")
    if self.no > len(f.break_label_stack):
        raise ierr.RuntimeExpressionError(f"dont have enough \
                loops to break out of")

    def dest(cnt):
        for dest_list in fc.dest_stack[-cnt:]:
            for td in dest_list:
                put_dest(self, fc, tc, td)

    # -1 because the last one is in front of the dest picking
    dest(self.no-1)
    ir.put_jump_to_label(
        f.break_label_stack[len(f.break_label_stack)-self.no], 
        fc
    )


# struct statements


@add_method_te_visit(sa.MemberDeclarationStatement)
def _(self: sa.MemberDeclarationStatement, tc: TypingContext,
        sc: context.StructContext):
    t = self.type_expr.te_visit(tc, sc)

    if self.name in sc.types:
        raise ierr.TypeExpressionError(f"redefinition of name {self.name}")

    sc.types[self.name] = t
    sc.members.append(self.name)

@add_method_te_visit(sa.TypeDeclarationStatementStruct)
def _(self: sa.TypeDeclarationStatementStruct, tc: TypingContext,
        sc: context.StructContext):
    t = self.type_expr.te_visit(tc, sc)

    if self.name != '_':
        if self.name in sc.types:
            raise ierr.TypeExpressionError(f"redefinition of name {self.name}")
        sc.types[self.name] = t

# value expressions

@add_method_te_visit(sa.IdExpression)
def _(self: sa.IdExpression, tc: TypingContext,
        fc: context.FunctionContext):
    mn = fc.scope_man.get_var_name(self.name)
    self.lvalue = True

    if mn is None:
        raise ierr.RuntimeExpressionError(f"Variable {self.name} not defined, at {self.linespan[0]}!")

    return mn


@add_method_te_visit(sa.IndexExpression)
def _(self: sa.IndexExpression, tc: TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, fc)
    ind = self.index.te_visit(tc, fc)
    self.lvalue = self.expr.lvalue

    if not isinstance(fc.types[e], ts.PointerType):
        raise ierr.RuntimeExpressionError(f"Can not offset a non-pointer type, at {self.linespan[0]}!")

    if not isinstance(fc.types[ind], ts.IntType):
        raise ierr.RuntimeExpressionError(f"Can not offset with a non-int type, at {self.linespan[0]}!")


    res = ir.get_pointer_offset(e, ind, fc)

    return res


#1
@add_method_te_visit(sa.MemberExpression)
def _(self: sa.MemberExpression, tc: TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, fc)
    if self.expr.lvalue:
        self.lvalue = self.expr.lvalue

    if not isinstance(fc.types[e], ts.StructType):
        raise ierr.RuntimeExpressionError(f"Can not index a non-struct type, at {self.linespan[0]}!")

    if self.member not in fc.types[e].members:
        raise ierr.RuntimeExpressionError(f"Can not index a non-existant struct member {self.member}, at {self.linespan[0]}!")

    if not self.expr.lvalue:
        put_dest(self, fc, tc, e)

    return ir.get_member(e, self.member, fc)


@add_method_te_visit(sa.DerefExpression)
def _(self: sa.DerefExpression, tc: TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, fc)
    self.lvalue = self.expr.lvalue

    if not isinstance(fc.types[e], ts.PointerType):
        raise ierr.RuntimeExpressionError(f"Can not dereference a non-pointer type, at {self.linespan[0]}!")

    return ir.get_dereference(e, fc)


@add_method_te_visit(sa.AddressExpression)
def _(self: sa.BinaryExpression, tc: TypingContext,
        fc: context.FunctionContext):
    e = self.expr.te_visit(tc, fc)
    self.lvalue = False

    if not self.expr.lvalue:
        raise ierr.RuntimeExpressionError(f"Taking address requires a lvalue, at {self.linespan[0]}!")

    return ir.get_address_of(e, fc)


@add_method_te_visit(sa.IntLiteralExpression)
def _(self: sa.IntLiteralExpression, tc: TypingContext,
        fc: context.FunctionContext):
    self.lvalue = False

    return ir.get_int_value(self.value, self.size, fc)


@add_method_te_visit(sa.BoolLiteralExpression)
def _(self: sa.BoolLiteralExpression, tc: TypingContext,
        fc: context.FunctionContext):
    self.lvalue = False

    return ir.get_bool_value(self.value, fc)

@add_method_te_visit(sa.CharLiteralExpression)
def _(self: sa.CharLiteralExpression, tc: TypingContext,
        fc: context.FunctionContext):
    self.lvalue = False

    return ir.get_char_value(self.value, fc)

@add_method_te_visit(sa.StringLiteralExpression)
def _(self: sa.StringLiteralExpression, tc: TypingContext,
        fc: context.FunctionContext):
    self.lvalue = False

    return ir.get_chars_ptr(self.value, fc)


@add_method_te_visit(sa.CallExpression)
def _(self: sa.CallExpression, tc: TypingContext,
        fc: context.FunctionContext):
    self.lvalue = False

    type_args_types = [t.te_visit(tc, fc) for t in self.type_expr_list]

    arg_names = [v.te_visit(tc, fc) for v in self.args]
    args_types = [fc.types[a] for a in arg_names]
    args_lvalues = [t.lvalue for t in self.args]

    try:
        func_call = tc.resolve_function(self.name, tuple(type_args_types), tuple(args_types))
    except ierr.InferenceError as e:
        raise ierr.InferenceError(f"Can not infer function call at {self.linespan[0]}") from e

    ret = get_func_call(self, fc, tc, func_call, arg_names, args_lvalues)
    return ret


# type expressions

@add_method_te_visit(sa.TypeAngleExpression)
def _(self: sa.TypeAngleExpression, tc: TypingContext,
        sfc: Union[context.StructContext, context.FunctionContext]):

    if self.name == "enable_if":
        if len(self.expr_list) != 1:
            raise ierr.TypeExpressionError(f"Enable_if has to have 1 expression only")
        else:
            t_expr = self.expr_list[0].te_visit(tc, sfc)
            if t_expr != ts.IntType(1):
                raise ierr.ChoiceSkipError(f"Failed enable_if: expr is not true(i1), skipping at {self.linespan[0]}")
            return t_expr

    if self.name == "enable_if_resolve":
        if len(self.expr_list) != 1:
            raise ierr.TypeExpressionError(f"Enable_if_resolve has to have 1 expression only")
        else:
            try:
                t_expr = self.expr_list[0].te_visit(tc, sfc)
            except ierr.InferenceError as e:
                raise ierr.ChoiceSkipError(f"Failed enable_if_resolve: error at resolution, skipping at {self.linespan[0]}") from e
            return t_expr

    texprs = [te.te_visit(tc, sfc) for te in self.expr_list]
    rt = tc.resolve_concrete(self.name, tuple(texprs))

    return rt

@add_method_te_visit(sa.TypeIdExpression)
def _(self: sa.TypeIdExpression, tc: TypingContext,
        sfc: Union[context.StructContext, context.FunctionContext]):

    # prefer a local name
    if isinstance(sfc, context.StructContext):
        if self.name in sfc.types:
            return sfc.types[self.name]
    if isinstance(sfc, context.FunctionContext):
        mn = sfc.scope_man.get_var_name(self.name)
        if mn is not None:
            return sfc.types[mn]

    # if no local name, go for a struct
    rt = tc.resolve_concrete(self.name, ())
    return rt

@add_method_te_visit(sa.TypeDerefExpression)
def _(self: sa.TypeDerefExpression, tc: TypingContext,
        sfc: Union[context.StructContext, context.FunctionContext]):

    e = self.expr.te_visit(tc, sfc)

    if isinstance(e, ts.PointerType):
        return e.pointed
    else:
        raise ierr.TypeExpressionError(f"Can not dereference a non-pointer type at {self.linespan[0]}!")


@add_method_te_visit(sa.TypePtrExpression)
def _(self: sa.TypePtrExpression, tc: TypingContext,
        sfc: Union[context.StructContext, context.FunctionContext]):

    e = self.expr.te_visit(tc, sfc)

    return ts.PointerType(e)


@add_method_te_visit(sa.TypeMemberExpression)
def _(self: sa.TypeMemberExpression, tc: TypingContext,
        sfc: Union[context.StructContext, context.FunctionContext]):

    e = self.expr.te_visit(tc, sfc)

    if not isinstance(e, ts.StructType):
        raise ierr.TypeExpressionError(f"Can not access a member type a type on a non-struct type!")
    return e.types[self.name]

