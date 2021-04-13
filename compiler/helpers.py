def tree_print_r(name, obj, prefix):
    if name is None:
        print(f"{prefix} ", end='')
    else:
        print(f"{prefix} {name} = ", end='')

    if hasattr(obj, "__dict__"):
        print(f"{type(obj).__name__}(")
        for k, v in obj.__dict__.items():
            tree_print_r(k, v, prefix+" - ")
        print(f"{prefix} )")
    elif type(obj) == list:
        print("[")
        for i in obj:
            tree_print_r(None, i, prefix+" - ")
        print(f"{prefix} ]")
    elif type(obj) == dict:
        print("{")
        for k,v in obj.items():
            tree_print_r(k, v, prefix+" - ")
        print(prefix+" }")
    else:
        print(f"{type(obj).__name__}({obj})")


def tree_print(obj):
    tree_print_r(None, obj, "")


def add_method(cls, name):
    def go(func):
        setattr(cls, name, func)
    return go

def add_method_to_list(target_list):
    def go(func):
        target_list.append(func)
    return go
