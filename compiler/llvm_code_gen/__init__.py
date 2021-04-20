def get_code(typing_result):
    from .generator import CodeGenerator
    cg = CodeGenerator(typing_result)
    cg.run()
    return cg.code
