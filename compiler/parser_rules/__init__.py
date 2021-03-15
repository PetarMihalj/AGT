class ParserRule:
    def rpn(self):
        for k,v in vars(self).items():
            if isinstance(v, ParserRule):
                setattr(self,k,v.rpn())
        print(self)
        return self
    def __init__(self, r):
        pass

import parser_rules.statements
import parser_rules.binary_expressions
import parser_rules.unary_expressions
import parser_rules.structural
import parser_rules.literals 
import parser_rules.operators 

modules = [statements,binary_expressions, unary_expressions, structural, literals, operators]

