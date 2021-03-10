from typing import List


def add(to_list: List):
    def f(cls: type):
        to_list.append(cls)
        return cls
    return f


def tree_print_r(obj, prefix):
    for k, v in obj.__dict__.items():
        if hasattr(v, "__dict__"):
            print(f"{prefix} {k} = (")
            tree_print_r(v, prefix+" - ")
            print(f"{prefix} )")
        else:
            print(f"{prefix} {k} = {v}")


def tree_print(obj):
    print("compilationUnit = (")
    tree_print_r(obj, "- ")
    print(")")
