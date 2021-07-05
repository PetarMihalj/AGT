def get_semantics_ast(syntax_ast):
    from .semantic_ast import SemanticEnvironment
    se = SemanticEnvironment()
    return syntax_ast.parse_semantics(se)
