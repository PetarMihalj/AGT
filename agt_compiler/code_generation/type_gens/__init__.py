def add_method_to_list(target_list):
    def go(func):
        target_list.append(func)
    return go

func_methods = []
struct_methods = []

from . import type_gens_init
from . import type_gens_io
from . import type_gens_lifetime
from . import type_gens_memory
from . import type_gens_misc
from . import type_gens_ops
from . import type_gens_typing
