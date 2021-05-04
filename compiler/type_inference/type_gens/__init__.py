from typing import Tuple

from .. import inference_errors as ierr
from .. import primitives as prim
from .. import type_system as ts
from .. import context
from ...semantics_parsing import semantic_ast as sa

from ...helpers import add_method_to_list

func_methods = []
struct_methods = []

from . import type_gens_init
from . import type_gens_io
from . import type_gens_lifetime
from . import type_gens_memory
from . import type_gens_misc
from . import type_gens_ops
from . import type_gens_typing
