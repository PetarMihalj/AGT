if __name__ == '__main__':
    import sys
    from ..syntax_parsing import get_syntax_ast
    from ..helpers import tree_print
    from . import get_semantics_ast

    data = open(sys.argv[1]).read()
    syntax_ast = get_syntax_ast(data)
    semantics_ast = get_semantics_ast(syntax_ast)
    tree_print(semantics_ast)
