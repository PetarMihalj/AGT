from typing import Tuple, List
from dataclasses import dataclass

from .. import inference_errors as ierr
from .. import type_system as ts
from .. import context
from ..code_blocks import Primitive 
from ..type_engine import TypingContext

from . import func_methods, concrete_methods, add_method_to_list

# --------------------------------------------------------

@add_method_to_list(func_methods)
def gen_heap_object(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "heap_object": raise ierr.TypeGenError()

    if len(type_argument_types) != 1: raise ierr.TypeGenError()
    init_type = type_argument_types[0]

    if isinstance(init_type, ts.StructType):
        init_type: ts.StructType
        if len(init_type.members) == 0:
            raise ierr.InferenceError("Cant allocate a struct without memebers")

    try:
        fn_alloc_mn = tc.resolve_function("heap_alloc", (init_type,), (ts.IntType(32),)).mangled_name
        fn_init_mn = tc.resolve_function("__init__", (), 
            (ts.PointerType(init_type),) + argument_types
        ).mangled_name
    except ierr.InferenceError as e:
        raise e

    dname = tc.scope_man.new_func_name(f"heap_object_init")
    tc.code_blocks.append(HeapObjectPrimitive(
        dname,
        init_type.mangled_name,
        [at.mangled_name for at in argument_types],
        fn_alloc_mn,
        fn_init_mn,
    ))

    ft = ts.FunctionType(
        dname, 
        ts.PointerType(init_type),
        do_not_copy_args = False,
    )
    return ft

@dataclass
class HeapObjectPrimitive(Primitive):
    fn_mn: str
    type_struct_mn: str
    types_mn: List[str]

    alloc_fn_i32_mn: str
    init_fn_mn: str

    def get_code(self):
        n = len(self.types_mn)

        args = ", ".join([f"%{self.types_mn[i]} %t_{i}" for i in range(n)])

        return [
                f"; Function Attrs: nofree norecurse nounwind sspstrong uwtable writeonly",
                f"define dso_local %{self.type_struct_mn}* @{self.fn_mn}({args}) local_unnamed_addr #0 {{",
                f"\t%ptr = call %{self.type_struct_mn}* @{self.alloc_fn_i32_mn}(i32 1)",
                f"\tcall void @{self.init_fn_mn}(%{self.type_struct_mn}* %ptr, {args})",
                f"\tret %{self.type_struct_mn}* %ptr",
                f"}}",
            ]

# --------------------------------------------------------


@add_method_to_list(func_methods)
def gen_stack_object(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "object": raise ierr.TypeGenError()
    if len(type_argument_types) != 1: raise ierr.TypeGenError()

    init_type = type_argument_types[0]
    if isinstance(init_type, ts.StructType):
        init_type: ts.StructType
        if len(init_type.members) == 0:
            raise ierr.InferenceError("Cant allocate a struct without memebers")

    try:
        fn_init_mn = tc.resolve_function("__init__", (), 
            (ts.PointerType(init_type),) + argument_types
        ).mangled_name
    except ierr.InferenceError as e:
        raise e

    dname = tc.scope_man.new_func_name(f"stack_object_init")
    tc.code_blocks.append(StackObjectPrimitive(
        dname,
        init_type.mangled_name,
        [at.mangled_name for at in argument_types],
        fn_init_mn,
    ))

    ft = ts.FunctionType(
        dname, 
        init_type,
        do_not_copy_args = False,
    )
    return ft

@dataclass
class StackObjectPrimitive(Primitive):
    fn_mn: str
    type_struct_mn: str
    types_mn: List[str]

    init_fn_mn: str

    def get_code(self):
        n = len(self.types_mn)

        args = ", ".join([f"%{self.types_mn[i]} %t_{i}" for i in range(n)])

        return [
                f"; Function Attrs: nofree norecurse nounwind sspstrong uwtable writeonly",
                f"define dso_local %{self.type_struct_mn} @{self.fn_mn}({args}) local_unnamed_addr #0 {{",
                f"\t%ptr = alloca %{self.type_struct_mn}",
                f"\tcall void @{self.init_fn_mn}(%{self.type_struct_mn}* %ptr, {args})",
                f"\t%item = load %{self.type_struct_mn}, %{self.type_struct_mn}* %ptr",
                f"\tret %{self.type_struct_mn} %item",
                f"}}",
            ]
