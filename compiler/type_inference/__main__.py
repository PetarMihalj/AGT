import sys

if __name__ == '__main__':
    from ..syntax_parsing import get_syntax_ast
    from ..helpers import tree_print
    from ..semantics_parsing import get_semantics_ast
    from . import get_typed_program

    data = open(sys.argv[1]).read()
    syntax_ast = get_syntax_ast(data)
    semantics_ast = get_semantics_ast(syntax_ast)

    tr = get_typed_program(semantics_ast)
    print("\n"*3+"LOGS")
    tr.recursive_logger.print_logs()
    print("\n"*3+"PRIMS")
    tree_print(tr.code_blocks)
    print("\n"*3)

    print(f"SUCC = {tr.main_name is not None}")
