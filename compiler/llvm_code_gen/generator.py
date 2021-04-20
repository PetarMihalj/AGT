from ..type_inference import flat_ir
from ..type_inference import type_engine as te
from ..type_inference import TypingResult 


class CodeGenerator:
    def __init__(self, tr: TypingResult):
        self.tr: TypingResult = tr
        self.code = []

    def add_structs():
        for s in self.tr.struct_types:
            s: ts.StructType
            self.code.append(f"%{s.mangled_name} = type {{")
            for member in s.members:
                self.code.append(f"\t%{s.types[member].mangled_name}\t\t\t#{member}")
            self.code.append(f"}}")

    def run(self):
        pass

