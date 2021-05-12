from dataclasses import dataclass
from typing import List, Tuple

from . import type_system as ts
from . import context

class CodeBlock:
    pass

class Primitive(CodeBlock):
    def get_code(self):
        raise NotImplementedError()

@dataclass
class FuncTypeCodeBlock(CodeBlock):
    fc: context.FunctionContext

    def get_code(self):
        code = []
        p_names = ", ".join([" %"+self.fc.types[n].mangled_name+" %"+n for n in self.fc.parameter_names_ordered])
        ret_str = f'%{self.fc.return_type.mangled_name}' if self.fc.return_type is not None else "void"

        code.append(f'define dso_local {ret_str} @{self.fc.mangled_name} ({p_names}) {{')

        code.extend(self.fc.code)
        code.append('}')
        return code


@dataclass
class StructTypeCodeBlock(CodeBlock):
    sc: context.StructContext

    def get_code(self):
        code = []
        code.append(f"%{self.sc.mangled_name} = type {{")
        for i, member in enumerate(self.sc.members):
            comma = ','
            if i==len(self.sc.members)-1:
                comma=''
            code.append(f"\t{self.sc.types[member].mangled_name}{comma}\t\t\t;{member}")
        code.append(f"}}")
        return code
