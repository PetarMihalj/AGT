from . import flat_ir
from . import type_engine as te
from . import type_system as ts


class CodeGenerator:
    def __init__(self, tr: te.TypingResult):
        self.tr: te.TypingResult = tr
        self.code = []

    def add_codeblocks(self):
        for pr in self.tr.code_blocks:
            self.code.extend(
                pr.get_code()
            )

    def add_header(self):
        self.code += [
            "%i8 = type i8",
            "%i16 = type i16",
            "%i32 = type i32",
            "%i64 = type i64",
            "%bool = type i1",
            "%char = type i8",
            "",
            "; Function Attrs: nofree nounwind",
            "declare i32 @printf(i8* nocapture readonly, ...) local_unnamed_addr #1",
            "",
            "; Function Attrs: nofree nounwind",
            "declare i32 @__isoc99_scanf(i8* nocapture readonly, ...) local_unnamed_addr #2",
            ""
            "@.in_int_str = private unnamed_addr constant [5 x i8] c\"%lld\\00\", align 1",
            "@.out_int_str = private unnamed_addr constant [5 x i8] c\"%lld\\00\", align 1",
            "@.out_char_str = private unnamed_addr constant [3 x i8] c\"%c\\00\", align 1",
            "@.out_chararray_str = private unnamed_addr constant [3 x i8] c\"%s\\00\", align 1",
            "",

            "; Function Attrs: nounwind",
            "declare noalias i8* @malloc(i64) #1",
            "",
            "; Function Attrs: nounwind",
            "declare void @free(i8* nocapture) local_unnamed_addr #1",
        ]

    def add_footer(self):
        self.code+=[
            "define dso_local i32 @main() #0 {",
            f"\t%1 = call i32 @{self.tr.main_name}()",
            "\tret i32 %1",
            "}",
        ]

    def run(self):
        self.add_header()
        self.code.append("; END OF HEADER")
        self.code.append("")

        self.add_codeblocks()

        self.code.append("")
        self.code.append("; START OF HEADER")
        self.add_footer()
