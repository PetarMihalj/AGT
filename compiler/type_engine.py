from typing import Dict, List, Union
import lang_ast as la
from la import TypeExpression


# scope manager


separator = "_$_"


class ScopeManager:
    def __init__(self):
        self.scope_stack: List[dict[str]] = []
        self.label_cnt = 0
        self.tmp_var_cnt = 0
        self.var_cnt = 0
        self.func_cnt = 0
        self.struct_cnt = 0
        self.break_label_stack = []

    def begin_scope(self):
        self.scope_stack.append(dict())

    def end_scope(self):
        self.scope_stack.pop()

    def get_var_name(self, name: str):
        for s in reversed(self.scope_stack):
            if name in s:
                return s[name]

    def new_label_name(self, description=""):
        self.label_cnt += 1
        return f"label{description}{separator}{self.label_cnt}"

    def new_tmp_var_name(self, description=""):
        self.tmp_var_cnt += 1
        return f"tmp_var{description}{separator}{self.tmp_var_cnt}"

    def new_var_name(self, name):
        self.var_cnt += 1
        res_var = f"var{separator}{name}{separator}{self.var_cnt}"
        self.scope_stack[-1][name] = res_var
        return res_var

    def new_func_name(self, name):
        self.func_cnt += 1
        res_var = f"func{separator}{name}{separator}{self.func_cnt}"
        return res_var

    def new_struct_name(self, name):
        self.struct_cnt += 1
        res_var = f"struct{separator}{name}{separator}{self.struct_cnt}"
        return res_var


# types


class Type:
    pass


class FunctionType(Type):
    name: str
    type_locals: Dict[str, Type]

    parameter_names: List[str]
    return_type: Type
    statements: List[la.Statement]


class StructType(Type):
    name: str
    type_locals: Dict[str, Type]
    members: List[str]


class IntType(Type):
    size: int


class VoidType(Type):
    pass


class BoolType(Type):
    value: bool


# engine


class TypesDG:
    def __init__(self):
        self.dict: Dict[TypeExpression, Type] = {}
        self.resolution_methods = []

    def __getitem__(self, te: TypeExpression):
        if te in self.dict:
            return self.dict[te]
        else:
            for m in self.resolution_methods:
                res = m(te)
                if res is not None:
                    return res
        return None

    def __setitem__(self, te: TypeExpression, t: Type):
        self.dict[te] = t


class DefinitionDG:
    def __init__(self, defs):
        self.defs: List[Union[la.FunctionDefinition,
                              la.StructDefinition]] = defs
        self.resolution_methods = []

    def __getitem__(self, te: TypeExpression) -> \
            List[Union[la.FunctionDefinition, la.StructDefinition]]:
        poss = []

        if isinstance(te, la.CallExpression):
            te: la.CallExpression
            for d in self.defs:
                if isinstance(d, la.FunctionDefinition):
                    d: la.FunctionDefinition
                    if te.name == d.name and\
                            len(te.type_expr_list) <= len(d.type_parameters)\
                            and len(te.args) == len(d.parameters):
                        poss.append(d)

                elif isinstance(d, la.StructDefinition):
                    d: la.StructDefinition
                    if te.name == d.name and\
                            len(te.type_expr_list) <= \
                            len(d.type_parameter_names):
                        poss.append(d)
        for m in self.resolution_methods:
            res = m(te)
            if res is not None:
                poss.append(res)
        return poss


class TypeEngine:
    def __init__(self, defs):
        self.scope_man = ScopeManager()
        self.types_dg = TypesDG()
        self.defs_dg = DefinitionDG(defs)

        self.stack = []

    def run(self):
        pass

    def try_to_eval_def(self, d:
                        Union[la.StructDefinition, la.FunctionDefinition]):
        pass


if __name__ == "__main__":
    te = TypeEngine()
    te.run()
