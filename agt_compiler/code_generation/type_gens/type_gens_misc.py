from typing import Tuple
from dataclasses import dataclass

from .. import inference_errors as ierr
from ..code_blocks import Primitive 
from .. import type_system as ts
from .. import context
from ...semantics_parsing import semantic_ast as sa

from ...helpers import add_method_to_list
from . import func_methods, struct_methods

from ..type_engine import TypingContext

# -------------------------------------------------------

@add_method_to_list(func_methods)
def gen_cast_ints(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "cast": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()
    if len(type_argument_types) != 1: raise ierr.TypeGenError()

    type_target = type_argument_types[0]
    type_source = argument_types[0]

    allowed = [ts.IntType(size) for size in [8,16,32,64]]
    if type_target not in allowed or type_source not in allowed:
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"dummy_cast_{type_source.size}_to_{type_target.size}")
    tc.code_blocks.append(CastIntTypes(
        dname,
        type_target.size,
        type_source.size,
    ))

    ft = ts.FunctionType(
        dname, 
        type_target,
        do_not_copy_args = False,
    )
    return ft

@dataclass
class CastIntTypes(Primitive):
    mangled_name: str
    target_size: int
    source_size: int
    def get_code(self):
        if self.target_size < self.source_size:
            return [
                f"; Function Attrs: norecurse nounwind readnone sspstrong uwtable",
                f"define dso_local i{self.target_size} @{self.mangled_name}(i{self.source_size} %0) local_unnamed_addr #0 {{",
                f"\t%2 = trunc i{self.source_size} %0 to i{self.target_size}",
                f"\tret i{self.target_size} %2",
                f"}}",
            ]
        elif self.target_size > self.source_size:
            return [
                f"; function attrs: norecurse nounwind readnone sspstrong uwtable",
                f"define dso_local i{self.target_size} @{self.mangled_name}(i{self.source_size} %0) local_unnamed_addr #0 {{",
                f"\t%2 = sext i{self.source_size} %0 to i{self.target_size}",
                f"\tret i{self.target_size} %2",
                f"}}",
            ]
        else:
            return [
                f"; function attrs: norecurse nounwind readnone sspstrong uwtable",
                f"define dso_local i{self.target_size} @{self.mangled_name}(i{self.source_size} %0) local_unnamed_addr #0 {{",
                f"\tret i{self.target_size} %0",
                f"}}",
            ]

# -------------------------------------------------------

@add_method_to_list(func_methods)
def gen_cast_bool_to_int(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "cast": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()
    if len(type_argument_types) != 1: raise ierr.TypeGenError()

    type_target = type_argument_types[0]
    type_source = argument_types[0]

    allowed = [ts.IntType(size) for size in [8,16,32,64]]
    if type_target not in allowed or type_source not in [ts.BoolType()]:
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"dummy_cast_bool_to_i{type_target.size}")
    tc.code_blocks.append(CastBoolToInt(
        dname,
        type_target.size,
    ))

    ft = ts.FunctionType(
        dname, 
        type_target,
        do_not_copy_args = False,
    )
    return ft

@dataclass
class CastBoolToInt(Primitive):
    mangled_name: str
    target_size: int
    def get_code(self):
        return [
            f"; Function Attrs: norecurse nounwind readnone sspstrong uwtable",
            f"define dso_local i{self.target_size} @{self.mangled_name}(i1 %0) local_unnamed_addr #0 {{",
            f"\t%2 = zext i1 %0 to i{self.target_size}",
            f"\tret i{self.target_size} %2",
            f"}}",
        ]

# ----------------------------------------------------------

@add_method_to_list(func_methods)
def gen_cast_int_to_bool(
                tc: TypingContext,
                name: str,
                type_argument_types: Tuple[ts.Type],
                argument_types: Tuple[ts.Type],
            ):
    if name != "cast": raise ierr.TypeGenError()
    if len(argument_types)!=1: raise ierr.TypeGenError()
    if len(type_argument_types) != 1: raise ierr.TypeGenError()

    type_target = type_argument_types[0]
    type_source = argument_types[0]

    allowed = [ts.IntType(size) for size in [8,16,32,64]]
    if type_source not in allowed or type_target not in [ts.BoolType()]:
        raise ierr.TypeGenError()

    dname = tc.scope_man.new_func_name(f"dummy_cast_i{type_source.size}_to_bool")
    tc.code_blocks.append(CastIntToBool(
        dname,
        type_source.size,
    ))

    ft = ts.FunctionType(
        dname, 
        type_target,
        do_not_copy_args = False,
    )
    return ft

@dataclass
class CastIntToBool(Primitive):
    mangled_name: str
    source_size: int
    def get_code(self):
        return [
            f"; Function Attrs: norecurse nounwind readnone sspstrong uwtable",
            f"define dso_local i1 @{self.mangled_name}(i{self.source_size} %0) local_unnamed_addr #0 {{",
            f"\t%2 = trunc i{self.source_size} %0 to i1",
            f"\tret i1 %2",
            f"}}",
        ]
