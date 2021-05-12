from typing import List
from . import type_system as ts
from . import context

# operations on stack symbolic registers

def put_stack_allocate(dest: str, ty: ts.Type, fc: context.FunctionContext):
    """
    Dest becomes an stack symbolic register with a value of type s.
    """
    fc.types[dest] = ty
    fc.code.extend([
        f"\t%{dest} = alloca %{ty.mangled_name}",
    ])

def get_stack_allocate_tmp(desc: str, ty: ts.Type, fc: context.FunctionContext):
    """
    Dest becomes an stack symbolic register with a value of type s.
    """
    dest = fc.scope_man.new_tmp_var_name(desc)
    fc.types[dest] = ty

    fc.code.extend([
        f"\t%{dest} = alloca %{ty.mangled_name}",
    ])
    return dest

def put_stack_copy(dest: str, src: str, fc: context.FunctionContext):
    """
    Src has to be a stack symbolic register with a value of type s.
    Dest has to be a stack symbolic register with a value of type s.
    """
    tmp = fc.scope_man.new_tmp_var_name("")
    s = fc.types[dest].mangled_name

    fc.code.extend([
        f"\t%{tmp} = load %{s}, %{s}* %{src}",
        f"\tstore %{s} %{tmp}, %{s}* %{dest}",
    ])

def put_param_to_stack_store(desc: str, ty: ts.Type, fc: context.FunctionContext):
    """
    Dest becomes a stack symbolic register with a value of type s.
    """
    mn = fc.scope_man.new_var_name(desc)

    pp = fc.scope_man.new_tmp_var_name("param_placeholder")
    fc.types[pp] = ty
    fc.parameter_names_ordered.append(pp)

    fc.types[mn] = ty
    fc.code.extend([
        f"\t%{mn} = alloca %{ty.mangled_name}",
        f"\tstore %{ty.mangled_name} %{pp}, %{ty.mangled_name}* %{mn}",
    ])

# functional


#1
def get_dereference(src: str, fc: context.FunctionContext):
    """
    Src has to be a stack symbolic register with a value of type PointerType(d).

    RETURNS a stack symbolic register with a value of type d
    """
    dest = fc.scope_man.new_tmp_var_name("deref")
    fc.types[dest]=fc.types[src].pointed

    stmn = fc.types[src].mangled_name
    dtmn = fc.types[dest].mangled_name

    fc.code.extend([
        f"\t%{dest} = load %{dtmn}*, %{stmn}* %{src}",
    ])
    return dest


#1
def get_address_of(src: str, fc: context.FunctionContext):
    """
    Src has to be a stack symbolic register with a value of type s.

    RETURNS a stack symbolic register with a value of type PointerType(s)
    """

    dest = fc.scope_man.new_tmp_var_name("addrof")
    fc.types[dest]=ts.PointerType(fc.types[src])

    stmn = fc.types[src].mangled_name
    dtmn = fc.types[dest].mangled_name

    fc.code.extend([
        f"\t%{dest} = alloca %{dtmn}",
        f"\tstore %{stmn}* %{src}, %{dtmn}* %{dest}"
    ])
    return dest

# pointer control

#1
def get_pointer_offset(src: str, offset: str, fc: context.FunctionContext):
    """
    Src has to be a stack symbolic register with a value of type PointerType(s)
    offset has to be a stack symbolic register with a value of type IntType(size from [8,16,32,64])

    RETURNS a stack symbolic register with a value of type PointerType(s) 
    """

    dest = fc.scope_man.new_tmp_var_name("ptroffset")
    fc.types[dest]=fc.types[src]

    ptmn = fc.types[src].mangled_name
    itmn = fc.types[src].pointed.mangled_name
    size = fc.types[offset].size

    tmp_val = fc.scope_man.new_tmp_var_name()
    tmp_ext_val = fc.scope_man.new_tmp_var_name()

    tmp_ptr = fc.scope_man.new_tmp_var_name()
    tmp_newptr = fc.scope_man.new_tmp_var_name()

    fc.code.extend([
        f"\t%{dest} = alloca %{ptmn}",

        f"\t%{tmp_val} = load i{size}, i{size}* %{offset}",
        f"\t%{tmp_ext_val} = sext i{size} %{tmp_val} to i64",

        f"\t%{tmp_ptr} = load %{ptmn}, %{ptmn}* %{src}",
        f"\t%{tmp_newptr} = getelementptr inbounds %{itmn}, %{ptmn} %{tmp_ptr}, i64 %{tmp_ext_val}",

        f"\tstore %{ptmn} %{tmp_newptr}, %{ptmn}* %{dest}",
    ])
    return dest

#1
def get_member(src: str, member_name: str, fc: context.FunctionContext):
    """
    Src has to be a stack symbolic register with a value of type s

    RETURNS a stack symbolic register with a value of type m same as the type of s.member_name
    """

    dest = fc.scope_man.new_tmp_var_name("member")
    fc.types[dest] = fc.types[src].types[member_name]

    stmn = fc.types[src].mangled_name
    ind = fc.types[src].members.index(member_name)

    fc.code.extend([ 
        f"%{dest} = getelementptr inbounds %{stmn}, %{stmn}* %{src}, i32 0, i32 {ind}"
    ])
    return dest

#1
def get_int_value(value: str, size: int, fc: context.FunctionContext):
    """
    RETURNS a stack symbolic register with a value of type i{size}.
    """
    dest = fc.scope_man.new_tmp_var_name("intval")
    fc.types[dest] = ts.IntType(size)

    fc.code.extend([
        f"\t%{dest} = alloca i{size}",
        f"\tstore %i{size} {value}, %i{size}* %{dest}"
    ])
    return dest

#1
def get_bool_value(value: bool, fc: context.FunctionContext):
    """
    RETURNS a stack symbolic register with a value of type i{size}.
    """
    dest = fc.scope_man.new_tmp_var_name("boolval")
    fc.types[dest] = ts.BoolType()

    value = 1 if value else 0

    fc.code.extend([
        f"\t%{dest} = alloca i1",
        f"\tstore i1 {value}, i1* %{dest}"
    ])
    return dest

#1
def get_char_value(value: str, fc: context.FunctionContext):
    """
    RETURNS a stack symbolic register with a value of type char.
    """
    dest = fc.scope_man.new_tmp_var_name("charval")
    fc.types[dest] = ts.CharType()

    fc.code.extend([
        f"\t%{dest} = alloca %char",
        f"\tstore %char {value}, %char* %{dest}"
    ])
    return dest

#1
def get_chars_ptr(chars: str, fc: context.FunctionContext):
    """
    RETURNS a stack symbolic register with a value of type PointerType(char).
    """
    ptr = fc.scope_man.new_tmp_var_name("chararrptr")
    ptr0 = fc.scope_man.new_tmp_var_name("chararrptr0")
    arr = fc.scope_man.new_tmp_var_name("chararrarr")
    fc.types[ptr] = ts.PointerType(ts.CharType())

    fc.code.extend([
        f"\t%{arr} = alloca [{len(chars)} x i8], align 1",
    ])
    for i,d in enumerate(chars):
        tmpptr = fc.scope_man.new_tmp_var_name("tmpptr")
        fc.code.extend([
            f"\t%{tmpptr} = getelementptr inbounds [{len(chars)} x i8], [{len(chars)} x i8]* %{arr}, i64 0, i64 {i}",
            f"\tstore i8 {d}, i8* %{tmpptr}, align 1",
        ])

    fc.code.extend([
        f"\t%{ptr0} = getelementptr inbounds [{len(chars)} x i8], [{len(chars)} x i8]* %{arr}, i64 0, i64 0",
        f"\t%{ptr} = alloca i8*",
        f"\tstore i8* %{ptr0}, i8** %{ptr}"
    ])
    return ptr


#1
def get_function_call(fn_to_call: ts.FunctionType, argument_names: List[str], fc: context.FunctionContext):
    """
    DOES NOT COPY stack symbolic registers!

    argument_names should be located in stack symbolic registers [argument_names]
    
    RETURNS a stack symbolic register which the result is saved into or None
    """
    if fn_to_call.return_type is not None:
        dest = fc.scope_man.new_tmp_var_name("funcres")
        fc.code.append(f"%{dest} = alloca %{fn_to_call.return_type.mangled_name}")
        fc.types[dest] = fn_to_call.return_type

    tmps = [fc.scope_man.new_tmp_var_name() for an in argument_names]
    types = [fc.types[an].mangled_name for an in argument_names]

    derefs = [f"\t%{tmp} = load %{ty}, %{ty}* %{an}" 
        for an,tmp,ty in zip(argument_names, tmps, types)]

    args_str = ", ".join([f"%{ty} %{tmp}" for tmp,ty in zip(tmps,types)])


    if fn_to_call.return_type is None:
        fc.code.extend(derefs+[
            f"\tcall void @{fn_to_call.mangled_name}({args_str})",
        ])
        return None
    else:
        dest_tmp = fc.scope_man.new_tmp_var_name()

        fc.code.extend(derefs+[
            f'\t%{dest_tmp} = call %{fn_to_call.return_type.mangled_name} @{fn_to_call.mangled_name}({args_str})',
            f'\tstore %{fn_to_call.return_type.mangled_name} %{dest_tmp}, %{fn_to_call.return_type.mangled_name}* %{dest}'
        ])
        return dest

# flow control

#2
def put_function_return(fc: context.FunctionContext):
    """
    Generates the code to exit the function with a value located in a stack symbolic register return or void
    """

    if fc.return_type is None:
        fc.code.extend([
            "\tret void"
        ])
    else:
        tmp = fc.scope_man.new_tmp_var_name("rettmp")
        ty = fc.types["return"].mangled_name
        fc.code.extend([
            f'\t%{tmp} = load %{ty}, %{ty}* %return',
            f'\tret %{ty} %{tmp}',
        ])


#2
def put_label(name: str, fc: context.FunctionContext):
    """
    Generates the code which defines a label
    """

    fc.code.extend([
        f"\t{name}:",
    ])


#2
def put_jump_to_label_conditional(var_name: str, label_true: str, label_false: str, fc: context.FunctionContext):
    """
    var_name has to be a stack symbolic register with a value of type s = bool.
    label_true and label_false have to be existant label names
    """

    tmp = fc.scope_man.new_tmp_var_name("jumptmp")

    fc.code.extend([
        f"\t%{tmp} = load i1, i1* %{var_name}",
        f"\tbr i1 %{tmp}, label %{label_true}, label %{label_false}",
    ])

#2
def put_jump_to_label(label: str, fc: context.FunctionContext):
    """
    label has to be an existant label name
    """

    fc.code.extend([
        f"\tbr label %{label}",
    ])

#2
def put_comment(comment: str, fc: context.FunctionContext):
    """
    Generates nonfunctional code with a comment 
    """

    fc.code.extend([
        f"\t; {comment}",
    ])
