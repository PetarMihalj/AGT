import ply.yacc as yacc
import token_rules
from dataclasses import dataclass
from types import MethodType
from typing import Union, List


def add(to_list: List):
    def f(cls: type):
        to_list.append(cls)
        return cls
    return f


def tree_print_r(obj, prefix):
    for k, v in obj.__dict__.items():
        if hasattr(v, "__dict__"):
            print(f"{prefix} {k} = (")
            tree_print_r(v, prefix+" - ")
            print(f"{prefix} )")
        else:
            print(f"{prefix} {k} = {v}")

def tree_print(obj):
    print("compilationUnit = (")
    tree_print_r(obj, "- ")
    print(")")


rl = []

# ----- Literals


@add(rl)
class IntLiteral:
    '''IntLiteral : INTL'''
    value: int
    signed: bool
    size: int

    def __init__(self, r):
        self.signed = True
        self.size = 32
        if 'u' in r[0]:
            self.signed = False
            sp = r[0].split('u')
            self.value = int(sp[0])
            if len(sp[1]) > 0:
                self.size = int(sp[1])
        elif 'i' in r[0]:
            sp = r[0].split('i')
            self.value = int(sp[0])
            if len(sp[1]) > 0:
                self.size = int(sp[1])
        else:
            self.value = int(r[0])


@add(rl)
class CharLiteral:
    '''CharLiteral : CHARL'''
    value: int

    def __init__(self, r):
        self.value = ord(r[0][1])


@add(rl)
class BoolLiteral:
    '''BoolLiteral : BOOLL'''
    value: bool

    def __init__(self, r):
        self.value = r[0] in ('True', 'true')


@add(rl)
class Literal:
    '''Literal : IntLiteral
               | BoolLiteral
               | CharLiteral
    '''
    value: Union[IntLiteral, CharLiteral, BoolLiteral]

    def __init__(self, r):
        self.value = r[0]


# ----- values


@dataclass
class Rvalue:
    value: Union[Literal, "FunctionCall", "Expression"]


@dataclass
class Lvalue:
    value: "ID"

# ----- Operators


@dataclass
class UnaryOperator:
    value: str


@ dataclass
class MultiplicativeOperator:
    value: str


@ dataclass
class AdditiveOperator:
    value: str


@ dataclass
class RelationalOperator:
    value: str

# ----- Unary expressions


@dataclass
class IncrementAfter:
    value: Lvalue


@dataclass
class IncrementBefore:
    value: Lvalue


@dataclass
class DecrementAfter:
    value: Lvalue


@dataclass
class DecrementBefore:
    value: Lvalue


@dataclass
class Negate:
    value: Union[Rvalue, Lvalue]

# -----  Multiplicative expressions


@dataclass
class MultiplyExpression:
    left: Union[Rvalue, Lvalue]
    right: "MultiplyExpression"

# ----- Expression


@ dataclass
class UnaryExpression:
    value: str


@ dataclass
class Factor:
    value: object
    next: 'Factor'


@ dataclass
class Expression:
    term: "Term"
    operator: str
    next: "Expression"


@ dataclass
class Term:
    factor: "Factor"
    next: 'Term'

# ----- globals


@add(rl)
class FunctionDefinition:
    """FunctionDefinition : TypeName ID '(' ParameterList ')' Block"""
    returnType: "TypeName"
    name: str
    parameterlist: "ParameterList"
    block: "Block"

    def __init__(self, r):
        self.returnType = r[0]
        self.name = r[1]
        self.parameterList = r[3]
        self.block = r[5]


@add(rl)
class DefinitionList:
    '''DefinitionList : FunctionDefinition DefinitionList
                      | empty
    '''
    functionDefinition: FunctionDefinition
    nxt: "DefinitionList"

    def __init__(self, r):
        if len(r) == 1:
            self.functionDefinition = None
            self.nxt = None
        else:
            self.functionDefinition = r[0]
            self.nxt = r[1]


@add(rl)
class CompilationUnit:
    '''CompilationUnit : DefinitionList'''
    definitionList: DefinitionList

    def __init__(self, r):
        self.definitionList = r[0]

# -----


@add(rl)
class TypeName:
    '''TypeName : ID'''
    name: str

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class Parameter:
    """Parameter : TypeName ID"""
    typeName: TypeName
    name: str

    def __init__(self, r):
        self.typeName = r[0]
        self.name = r[1]


@add(rl)
class ParameterList:
    """ParameterList : Parameter ',' ParameterList
                     | Parameter
                     | empty
    """
    parameter: "Parameter"
    nxt: "ParameterList"

    def __init__(self, r):
        if r[0] == 'empty':
            self.parameter = None
            self.nxt = None
        elif len(r) == 1:
            self.parameter = r[0]
            self.nxt = None
        else:
            self.parameter = r[0]
            self.nxt = r[1]

# ----- statements


@ dataclass
class StatementList:
    statement: "Statement"
    next: "StatementList"


@ dataclass
class Statement:
    pass


@add(rl)
class Block:
    "Block : '{' '}'"

    def __init__(self, r):
        pass


@ dataclass
class IfStatement:
    condition: Expression
    block: StatementList


@ dataclass
class ElseStatement:
    block: StatementList


@ dataclass
class AssignmentStatement:
    left: str
    right: Expression


class Parser:
    def __init__(self, lexer, rules_list, **kwargs):
        for cls in rules_list:
            self.injectRule(cls)
            print(f"Injected {cls}")

        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer)

    def injectRule(self, rule_class):
        def method(self, p):
            obj = rule_class(p[1:])
            p[0] = obj
        bound = MethodType(method, self)
        bound.__func__.__doc__ = rule_class.__doc__
        self.__setattr__(f"p_{rule_class}", bound)

    def p_empty(self, p):
        '''empty :'''
        pass

    start = 'CompilationUnit'


if __name__ == '__main__':
    data = '''
    void a(u32 p){}
    '''
    lexer = token_rules.Lexer()
    lexer.test(data)
    parser = Parser(lexer, rl, debug=True)
    a = parser.parse(data)
    tree_print(a)
