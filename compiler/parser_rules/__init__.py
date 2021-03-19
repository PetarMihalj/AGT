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
import parser_rules.expressions
import parser_rules.structural
import parser_rules.atomic 

modules = [statements,expressions,  structural, atomic]

