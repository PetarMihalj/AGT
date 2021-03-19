from parser_rules import ParserRule

class CompilationUnit(ParserRule):
    '''CompilationUnit : DefinitionListR'''

    def __init__(self, r):
        self.definitionList = r[0]

class DefinitionListR(ParserRule):
    '''DefinitionListR : FunctionDefinition DefinitionListR
                       | StructDefinition DefinitionListR
                       | empty
    '''

    def __init__(self, r):
        if len(r) == 1:
            self.definition = None
            self.nxt = None
        else:
            self.definition = r[0]
            self.nxt = r[1]

    def rpn(self):
        if self.definition == None:
            return []
        else:
            return [self.definition.rpn()] + self.nxt.rpn()

class FunctionDefinition(ParserRule):
    """FunctionDefinition : Id Id '(' ParameterListR ')' Block"""

    def __init__(self, r):
        self.returnType = r[0]
        self.name = r[1]
        self.parameterList = r[3]
        self.block = r[5]

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

class Parameter(ParserRule):
    """Parameter : Id Id"""

    def __init__(self, r):
        self.typeName = r[0]
        self.name = r[1]

class Block(ParserRule):
    "Block : '{' StatementListR '}'"

    def __init__(self, r):
        self.statementList = r[1]

class StructDefinition(ParserRule):
    """StructDefinition : STRUCT Id '(' ParameterListR ')'"""

    def  __init__(self, r):
        self.typeName = r[1]
        self.parameterList = r[3]



