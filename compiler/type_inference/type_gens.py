from typing import List

from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts

from ..semantics_parsing import semantic_ast as sa
# MAIN METHODS

func_methods = []
struct_methods = []

def gen_function(tc, name: str,
                 type_argument_types: List[Type],
                 argument_types: List[Type]
            ):
    if ((name, tuple(type_argument_types), tuple(argument_types))) in tc.gen_set:
        return
    tc.gen_set.add((name, tuple(type_argument_types), tuple(argument_types)))
    for sm in func_methods:
        sm(tc,name,type_argument_types, argument_types)

def gen_struct(tc, name: str,
            type_argument_types: List[Type]
        ):
    if ((name, tuple(type_argument_types))) in tc.gen_set:
        return
    tc.gen_set.add((name, tuple(type_argument_types))) 
    for sm in struct_methods:
        sm(tc,name,type_argument_types)

from . import type_gens_lifetime
from . import type_gens_io
from . import type_gens_memory
from . import type_gens_misc
from . import type_gens_typing
from . import type_gens_ops
