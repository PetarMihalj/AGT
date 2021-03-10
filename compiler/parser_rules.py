import ply.yacc as yacc
import token_rules
from dataclasses import dataclass
from types import MethodType
from helpers import add, tree_print
from typing import Union

import literals


rl = []



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


@add(rl)
class IncrementAfter:
    """IncrementAfter : ID INC"""
    name: str

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class IncrementBefore:
    """IncrementBefore : INC ID"""
    name: str

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class DecrementAfter:
    """DecrementAfter : ID DEC"""
    name: str

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class DecrementBefore:
    """DecrementBefore : DEC ID"""
    name: str

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class Negate:
    """Negate : '-' ID"""
    name: str

    def __init__(self, r):
        self.name = r[0]


@add(rl)
class FunctionCall:
    """FunctionCall : ID '(' ArgumentListR ')'"""

    name: str
    argumentListR: "ArgumentListR"

    def __init__(self, r):
        self.name = r[0]
        self.argumentListR = r[2]


# -----  Multiplicative expressions


# ----- Expression


@add(rl)
class UnaryExpression:
    """UnaryExpression : Negate
                       | IncrementAfter
                       | IncrementBefore
                       | DecrementAfter
                       | DecrementBefore
                       | FunctionCall
                       | ID
                       | Literal
    """
    unaryExprValue: Union["Negate", "IncrementAfter",
                          "IncrementBefore",
                          "FunctionCall", "DecrementAfter", "DecrementBefore",
                          str, "Literal"]

    def __init__(self, r):
        self.unaryExprValue = r[0]


@add(rl)
class Expression:
    """Expression : UnaryExpression"""
    exprValue: Union[UnaryExpression]

    def __init__(self, r):
        self.exprValue = r[0]


class Factor:
    value: object
    next: 'Factor'


class Term:
    factor: "Factor"
    next: 'Term'

# ----- globals


@add(rl)
class Block:
    "Block : '{' StatementListR '}'"
    statementListR: "StatementListR"

    def __init__(self, r):
        self.statementListR = r[1]


@add(rl)
class FunctionDefinition:
    """FunctionDefinition : TypeName ID '(' ParameterListR ')' Block"""
    returnType: "TypeName"
    name: str
    parameterlistR: "ParameterListR"
    block: Block

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
    functionDefinition: FunctionDefinition
    nxt: "DefinitionListR"

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
    definitionListR: DefinitionListR

    def __init__(self, r):
        self.definitionListR = r[0]

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
class ParameterListR:
    """ParameterListR : Parameter ',' ParameterListR
                     | Parameter
                     | empty
    """
    parameter: "Parameter"
    nxt: "ParameterListR"

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
    expr: Expression

    def __init__(self, r):
        self.expr = r[0]


@add(rl)
class ArgumentListR:
    """ArgumentListR : Argument ',' ArgumentListR
                     | Argument
                     | empty
    """
    argument: "Argument"
    nxt: "ArgumentListR"

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


class Parser:
    def __init__(self, lexer, rules_list, **kwargs):
        for cls in rules_list:
            self.injectRule(cls)
            print(f"Injected {cls}")

        self.lexer = lexer
        self.tokens = lexer.tokens
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data, **kvargs):
        return self.parser.parse(data, lexer=self.lexer, **kvargs)

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
    void a(u32 p, u32 t){
        //for (a;432;a){a++;}
        while (a){
            a--;
        }
    }
    '''
    lexer = token_rules.Lexer()
    lexer.test(data)
    parser = Parser(lexer, rl, debug=True)
    a = parser.parse(data)
    tree_print(a)
