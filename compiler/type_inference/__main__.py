
if __name__ == '__main__':
    import sys
    from ..syntax_parsing import get_syntax_ast
    from ..helpers import tree_print
    from ..semantics_parsing import get_semantics_ast
    from . import get_typed_program

    data = open(sys.argv[1]).read()
    syntax_ast = get_syntax_ast(data)
    semantics_ast = get_semantics_ast(syntax_ast)

    tr = get_typed_program(semantics_ast)
    print("\n"*3+"LOGS")
    tr.logger.print_logs(log_level = 2)
    print("\n"*3+"FUNCTIONS")
    tree_print(tr.func_types)
    print("\n"*3+"STRUCTS")
    tree_print(tr.struct_types)
