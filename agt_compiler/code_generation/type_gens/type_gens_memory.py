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
def gen_heap_alloc(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "heap_alloc": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()

    if len(type_argument_types) != 1: raise ierr.TypeGenError()

    if not isinstance(argument_types[0], ts.IntType): raise ierr.TypeGenError()

    type_alloc = type_argument_types[0]
    type_size = argument_types[0]

    dname = tc.scope_man.new_func_name(f"dummy_heap_alloc_array")
    tc.code_blocks.append(HeapAllocPrimitive(
        dname,
        type_alloc.mangled_name,
        type_size.size
    ))

    ft = ts.FunctionType(
        dname, 
        ts.PointerType(type_alloc),
        do_not_copy_args = False,
    )
    return ft

@dataclass
class HeapAllocPrimitive(Primitive):
    mangled_name: str
    type_mangled_name: str
    size: int

    def get_code(self):
        return [
            f"; Function Attrs: noinline nounwind optnone sspstrong uwtable",
            f"define dso_local %{self.type_mangled_name}* @{self.mangled_name}(i{self.size} %0) #0 {{",
            f"\t%2 = alloca i{self.size}",
            f"\tstore i{self.size} %0, i{self.size}* %2",
            f"\t%3 = load i{self.size}, i{self.size}* %2",
            f"\t%4 = sext i{self.size} %3 to i64",
            "",
            f"\t%Size = getelementptr %{self.type_mangled_name}, %{self.type_mangled_name}* null, i32 1",
            f"\t%SizeI = ptrtoint %{self.type_mangled_name}* %Size to i64",
            "",
            f"\t%5 = mul i64 %SizeI, %4",
            f"\t%6 = call noalias i8* @malloc(i64 %5) #2",
            f"\t%7 = bitcast i8* %6 to %{self.type_mangled_name}*",
            f"\tret %{self.type_mangled_name}* %7",
            f"}}",
        ]

# ---------------------------------------------------------------------

@add_method_to_list(func_methods)
def gen_heap_free(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "heap_free": raise ierr.TypeGenError()
    if len(argument_types) != 1: raise ierr.TypeGenError()
    if len(type_argument_types) != 0: raise ierr.TypeGenError()

    type_free_ptr = argument_types[0]
    if not isinstance(type_free_ptr, ts.PointerType): raise ierr.TypeGenError()

    type_free = type_free_ptr.pointed

    dname = tc.scope_man.new_func_name(f"dummy_heap_free")
    tc.code_blocks.append(HeapFreePrimitive(
        dname,
        type_free.mangled_name,
    ))

    ft = ts.FunctionType(
        dname, 
        None,
        do_not_copy_args = False,
    )
    return ft

@dataclass
class HeapFreePrimitive(Primitive):
    mangled_name: str
    type_mangled_name: str
    def get_code(self):
        return [
            f"; Function Attrs: nounwind sspstrong uwtable",
            f"define dso_local void @{self.mangled_name}(%{self.type_mangled_name}* nocapture %0) local_unnamed_addr #0 {{",
            f"\t%2 = bitcast %{self.type_mangled_name}* %0 to i8*",
            f"\ttail call void @free(i8* %2) #2",
            f"\tret void",
            f"}}",
        ]
