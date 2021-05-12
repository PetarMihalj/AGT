from typing import List

separator = "$"

class DefinitionScopeManager:
    def __init__(self):
        self.scope_stack: List[dict[str]] = []

        self.var_cnt = 0
        self.tmp_var_cnt = 0
        self.label_cnt = 0

        self.func_cnt = 0
        self.struct_cnt = 0

    def get_size(self):
        return len(self.scope_stack)

    def begin_scope(self):
        self.scope_stack.append(dict())

    def end_scope(self):
        self.scope_stack.pop()

    # var names

    def new_var_name(self, name, type_name=False):
        if name in self.scope_stack:
            return None
        
        self.var_cnt += 1
        if type_name:
            res_var = f"type_var{separator}{name}{separator}{self.var_cnt}"
        else:
            res_var = f"var{separator}{name}{separator}{self.var_cnt}"
        if name in self.scope_stack[-1]:
            return None
        self.scope_stack[-1][name] = res_var
        return res_var

    def get_var_name(self, name: str):
        for s in reversed(self.scope_stack):
            if name in s:
                return s[name]
        return None

    def new_tmp_var_name(self, description="", type_name=False):
        self.tmp_var_cnt += 1
        if type_name:
            res_var = f"tmp_type_var{description}{separator}{self.tmp_var_cnt}"
        else:
            res_var = f"tmp_var{description}{separator}{self.tmp_var_cnt}"

        return res_var

    def new_label_name(self, description=""):
        self.label_cnt += 1
        return f"label{description}{separator}{self.label_cnt}"


class GlobalScopeManager:
    def __init__(self):
        self.func_cnt = 0
        self.struct_cnt = 0

    def new_func_name(self, name):
        self.func_cnt += 1
        res_var = f"func{separator}{name}{separator}{self.func_cnt}"
        return res_var

    def new_struct_name(self, name):
        self.struct_cnt += 1
        res_var = f"struct{separator}{name}{separator}{self.struct_cnt}"
        return res_var
