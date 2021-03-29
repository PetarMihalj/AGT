def without_nxt(node):
    keys = vars(node).keys()
    for k in keys:
        if k != "nxt":
            return getattr(node, k)


class FunctionDefinition:
    def __init__(self):
        self.name = None
        self.stack_declarations = []
        self.type_parameters = []
        self.parameters = []


class FunctionCall:
    def __init__(self):
        self.name = None
        self.type_arguments = []
        self.arguments = []


def flatten_lists(ast):
    if not hasattr(ast, "__dict__"):
        return
    for k, v in vars(ast).items():
        if hasattr(v, "nxt"):
            nl = [without_nxt(v)]
            while v.nxt is not None:
                v = v.nxt
                nl.append(without_nxt(v))
            setattr(ast, k, list(filter(None, nl)))
            for i in getattr(ast, k):
                flatten_lists(i)
        else:
            flatten_lists(v)


def flatten_definitions(ast):


if __name__ == '__main__':
    from lexer import Lexer
    from parser import Parser
    from helpers import tree_print
    data = open('prog1.st').read()
    lexer = Lexer()
    lexer.test(data)
    parser = Parser(lexer, debug=True)
    a = parser.parse(data)
    flatten_lists(a)
    tree_print(a)
