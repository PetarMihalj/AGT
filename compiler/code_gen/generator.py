from ..type_inference import flat_ir
from ..type_inference import type_engine as te
from ..type_inference import TypingResult 
from ..type_inference import type_system as ts


class CodeGenerator:
    def __init__(self, tr: TypingResult):
        self.tr: TypingResult = tr
        self.code = []

    def add_structs(self): 
        for s in self.tr.struct_types.values():
            if not isinstance(s, ts.StructType) or not s.needs_gen:
                continue
            s: ts.StructType
            self.code.append(f"{s.mangled_name} = type {{")
            for member in s.members:
                self.code.append(f"\t{s.types[member].mangled_name}\t\t\t#{member}")
            self.code.append(f"}}")

    def add_prims(self):
        for pr in self.tr.primitives:
            self.code.extend(
                pr.get_code(self.tr)
            )

    def add_header(self):
        self.code += [
            "; ModuleID = 'cprog.c'",
            "source_filename = \"cprog.c\"",
            "target datalayout = \"e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128\"",
            "target triple = \"x86_64-pc-linux-gnu\"",
        ]

    def add_footer(self):
        main_name = self.tr.func_types[("main",(),())].mangled_name
        self.code+=[
            "define dso_local i32 @main() #0 {",
            f"\t%1 = call i32 @{main_name}()",
            "\tret i32 %1",
            "}",
        ]

    def add_funcs(self):
        for f in self.tr.func_types.values():
            self.add_func(f)

    def add_func(self, f: ts.FunctionType):
        p_names = ", ".join([" %"+f.types[n].mangled_name+" %"+n for n in f.parameter_names_ordered])
        ret_str = f'%{f.types["return"].mangled_name}' if f.types["return"]!=ts.VoidType() else "void"

        self.code.append(f'define dso_local {ret_str} @{f.mangled_name} ({p_names}) {{')

        for fs in f.flat_statements:
            self.code+=fs.get_code(f)

        self.code.append('}')

    def run(self):
        self.add_header()

        self.code.append("")
        self.code.append("; Structs")
        self.code.append("")
        self.add_structs()

        self.code.append("")
        self.code.append("; Primitives")
        self.code.append("")
        self.add_prims()

        self.code.append("")
        self.code.append("; Funcs")
        self.code.append("")
        self.add_funcs()

        self.code.append("")
        self.code.append("; Footer")
        self.code.append("")
        self.add_footer()
