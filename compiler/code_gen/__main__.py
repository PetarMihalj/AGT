if __name__ == '__main__':
    import sys
    from ..syntax_parsing import get_syntax_ast
    from ..helpers import tree_print
    from ..semantics_parsing import get_semantics_ast
    from ..type_inference import get_typed_program
    from . import get_code

    data = open(sys.argv[1]).read()
    syntax_ast = get_syntax_ast(data)
    semantics_ast = get_semantics_ast(syntax_ast)
    tr = get_typed_program(semantics_ast)
    code = get_code(tr)
    for l in code:
        print(l)
