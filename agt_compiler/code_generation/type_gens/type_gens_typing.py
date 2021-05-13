from typing import Tuple, List
from dataclasses import dataclass

from .. import inference_errors as ierr
from .. import type_system as ts
from .. import context
from ..code_blocks import Primitive 
from ..type_engine import TypingContext

from . import func_methods, struct_methods, add_method_to_list

# ---------------------------------------------------------------------

@add_method_to_list(func_methods)
def gen_type_to_value(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "type_to_value": raise ierr.TypeGenError()
    if len(argument_types)>0: raise ierr.TypeGenError()

    if len(type_argument_types) != 2: raise ierr.TypeGenError()

    if not isinstance(type_argument_types[0], ts.IntType): raise ierr.TypeGenError()
    if not isinstance(type_argument_types[1], ts.IntType): raise ierr.TypeGenError()
    val = type_argument_types[0].size
    size = type_argument_types[1].size

    dname = tc.scope_man.new_func_name(f"dummy_ttv_{val}i{size}")
    tc.code_blocks.append(TypeToValuePrimitive(
        dname,
        val,
        size,
    ))

    ft = ts.FunctionType(
        dname, 
        ts.IntType(size),
        do_not_copy_args = False,
    )
    return ft

@dataclass
class TypeToValuePrimitive(Primitive):
    mangled_name: str
    value: int
    size: int

    def get_code(self):
        return [
            f"define dso_local i{self.size} @{self.mangled_name}() #0 {{",
            f"  ret i{self.size} {self.value}",
            f"}}",
        ]

# ---------------------------------------------------------------------

@add_method_to_list(struct_methods)
def gen_int_type(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
            ):
    if len(name)==0:
        raise ierr.TypeGenError()
    if len(type_argument_types)!=0:
        raise ierr.TypeGenError()
    if name[0] != 'i':
        raise ierr.TypeGenError()
    
    try:
        size = int(name[1:])
    except:
        raise ierr.TypeGenError()

    return ts.IntType(size)

# ---------------------------------------------------------------------

@add_method_to_list(struct_methods)
def gen_bool_type(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
            ):
    if name!='bool':
        raise ierr.TypeGenError()
    if len(type_argument_types)!=0:
        raise ierr.TypeGenError()
    
    return ts.BoolType()

# ---------------------------------------------------------------------

reducer = {
 '__eq__':(lambda x,y:x==y),
 '__ne__':(lambda x,y:x!=y),
 '__gt__':(lambda x,y:x>y),
 '__lt__':(lambda x,y:x<y),
 '__le__':(lambda x,y:x<=y),
 '__ge__':(lambda x,y:x>=y),

'__add__':(lambda x,y:x+y),
'__sub__':(lambda x,y:x-y),
'__mul__':(lambda x,y:x*y),
'__div__':(lambda x,y:x//y),
'__mod__':(lambda x,y:x%y),

 '__sand__':(lambda x,y:int(x!=0 and y!=0)),
 '__sor__':(lambda x,y:int(x!=0 or y!=0)),
 '__and__':(lambda x,y:int(x!=0 and y!=0)),
 '__or__':(lambda x,y:int(x!=0 and y!=0)),
}

@add_method_to_list(struct_methods)
def gen_int_type_ops(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
            ):
    if name not in reducer:
        raise ierr.TypeGenError()
    if len(type_argument_types) != 2:
        raise ierr.TypeGenError()
    if not isinstance(type_argument_types[0], ts.IntType):
        raise ierr.TypeGenError()
    if not isinstance(type_argument_types[1], ts.IntType):
        raise ierr.TypeGenError()

    i1 = type_argument_types[0].size
    i2 = type_argument_types[1].size
    try:
        res = reducer[name](i1, i2)
    except:
        raise ierr.TypeGenError()

    return ts.IntType(res)

@add_method_to_list(struct_methods)
def gen_int_type_not(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
            ):
    if name != "__not__": 
        raise ierr.TypeGenError()
    if len(type_argument_types) != 1:
        raise ierr.TypeGenError()
    if not isinstance(type_argument_types[0], ts.IntType):
        raise ierr.TypeGenError()

    i1 = type_argument_types[0].size
    try:
        res = int(i1 == 0)
    except:
        raise ierr.TypeGenError()

    return ts.IntType(res)

# ---------------------------------------------------------------------

@add_method_to_list(struct_methods)
def gen_struct_type_ops(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
            ):
    if len(type_argument_types) != 2:
        raise ierr.TypeGenError()
    t1 = type_argument_types[0]
    t2 = type_argument_types[1]

    # because there is a specialization for this already in gens
    if isinstance(type_argument_types[0], ts.IntType) and isinstance(type_argument_types[1], ts.IntType):
        raise ierr.TypeGenError()

    if name=="__eq__":
        return ts.IntType(int(t1 == t2))
    elif name=="__ne__":
        return ts.IntType(int(t1 != t2))
    else:
        raise ierr.TypeGenError()
