def tree_print_r(name, obj, prefix, dbg):
    if name is None:
        print(f"{prefix} ", end='')
    else:
        print(f"{prefix} {name} = ", end='')

    if hasattr(obj, "__dict__"):
        print(f"{type(obj).__name__}(")
        for k, v in obj.__dict__.items():
            if k not in ["linespan", "lexspan"] or dbg:
                tree_print_r(k, v, prefix+" - ", dbg)
        print(f"{prefix} )")
    elif type(obj) == list:
        print("[")
        for i in obj:
            tree_print_r(None, i, prefix+" - ", dbg)
        print(f"{prefix} ]")
    elif type(obj) == dict:
        print("{")
        for k,v in obj.items():
            tree_print_r(k, v, prefix+" - ", dbg)
        print(prefix+" }")
    else:
        print(f"{type(obj).__name__}({obj})")


def tree_print(obj, debugging_info = False):
    tree_print_r(None, obj, "", debugging_info)
