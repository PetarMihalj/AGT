from parser_rules import ParserRule

class Block(ParserRule):
    "Block : '{' StatementListR '}'"

    def __init__(self, r):
        self.statementList = r[1]


class FunctionDefinition(ParserRule):
    """FunctionDefinition : TypeName ID '(' ParameterListR ')' Block"""

    def __init__(self, r):
        self.returnType = r[0]
        self.name = r[1]
        self.parameterList = r[3]
        self.block = r[5]


class DefinitionListR(ParserRule):
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

    def rpn(self):
        if self.functionDefinition == None:
            return []
        else:
            return [self.functionDefinition.rpn()] + self.nxt.rpn()


class CompilationUnit(ParserRule):
    '''CompilationUnit : DefinitionListR'''

    def __init__(self, r):
        self.definitionList = r[0]

# -----


class TypeName(ParserRule):
    '''TypeName : ID'''

    def __init__(self, r):
        self.name = r[0]


class VarName(ParserRule):
    '''VarName : ID'''

    def __init__(self, r):
        self.name = r[0]
    def rpn(self):
        return self


class Parameter(ParserRule):
    """Parameter : TypeName ID"""

    def __init__(self, r):
        self.typeName = r[0]
        self.name = r[1]


class ParameterListR(ParserRule):
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

    def rpn(self):
        if self.parameter == None:
            return []
        elif self.nxt == None:
            return [self.parameter.rpn()]
        else:
            return [self.parameter.rpn()] + self.nxt.rpn()


class Argument(ParserRule):
    """Argument : Expression"""

    def __init__(self, r):
        self.expr = r[0]



class ArgumentListR(ParserRule):
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

    def rpn(self):
        if self.argument == None:
            return []
        elif self.argument == None:
            return [self.argument.rpn()]
        else:
            return [self.argument.rpn()] + self.nxt.rpn()
