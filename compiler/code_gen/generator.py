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
        pass

    def run(self):
        self.code.append("")
        self.code.append("# Header")
        self.code.append("")
        self.add_header()

        self.code.append("")
        self.code.append("# Primitives")
        self.code.append("")
        self.add_prims()

        self.code.append("")
        self.code.append("# Structs")
        self.code.append("")
        self.add_structs()

