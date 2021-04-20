if __name__ == '__main__':
    import sys
    from . import get_syntax_ast
    from .. import helpers

    data = open(sys.argv[1]).read()
    syn_ast = get_syntax_ast(data)
    helpers.tree_print(syn_ast)
