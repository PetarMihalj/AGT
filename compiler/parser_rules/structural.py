from helpers import add
rl = []


@add(rl)
class Block:
    "Block : '{' StatementListR '}'"

    def __init__(self, r):
        self.statementListR = r[1]


@add(rl)
class FunctionDefinition:
    """FunctionDefinition : TypeName ID '(' ParameterListR ')' Block"""

    def __init__(self, r):
        self.returnType = r[0]
        self.name = r[1]
        self.parameterListR = r[3]
        self.block = r[5]


@add(rl)
class DefinitionListR:
    '''DefinitionListR : FunctionDefinition DefinitionListR
                       | empty
    '''

    def __init__(self, r):
        if len(r) == 1:
            self.functionDefinition = None
            self.nxt = None
        else:
            self.functionDefinition = r[0]
            self.nxt = r[1]


@add(rl)
class CompilationUnit:
    '''CompilationUnit : DefinitionListR'''

    def __init__(self, r):
        self.definitionListR = r[0]

# -----


@add(rl)
class TypeName:
    '''TypeName : ID'''

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class VarName:
    '''VarName : ID'''

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class Parameter:
    """Parameter : TypeName ID"""

    def __init__(self, r):
        self.typeName = r[0]
        self.name = r[1]


@add(rl)
class ParameterListR:
    """ParameterListR : Parameter ',' ParameterListR
                     | Parameter
                     | empty
    """

    def __init__(self, r):
        if r[0] == 'empty':
            self.parameter = None
            self.nxt = None
        elif len(r) == 1:
            self.parameter = r[0]
            self.nxt = None
        else:
            self.parameter = r[0]
            self.nxt = r[2]


@add(rl)
class Argument:
    """Argument : Expression"""

    def __init__(self, r):
        self.expr = r[0]


@add(rl)
class ArgumentListR:
    """ArgumentListR : Argument ',' ArgumentListR
                     | Argument
                     | empty
    """

    def __init__(self, r):
        if r[0] == 'empty':
            self.argument = None
            self.nxt = None
        elif len(r) == 1:
            self.argument = r[0]
            self.nxt = None
        else:
            self.argument = r[0]
            self.nxt = r[2]
