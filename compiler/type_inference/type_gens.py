from typing import List

from . import primitives as prim
from .type_system import Type
from ..helpers import add_method_to_list
from . import type_system as ts

from ..semantics_parsing import semantic_ast as sa

func_methods = []
struct_methods = []

from . import type_gens_lifetime
from . import type_gens_io
from . import type_gens_memory
from . import type_gens_misc
from . import type_gens_typing
from . import type_gens_ops
