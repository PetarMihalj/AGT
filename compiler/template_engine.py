from parser import Parser, flatten_lists
from lexer import Lexer
from helpers import tree_print
import parser_rules


class TemplateEngine:
    def __init__(self, ast):
        self.ast = ast

    def extract_definitions(self):
        for d in self.ast.definitionList:
            if isinstance(d, parser_rules.FunctionDefinition):


if __name__ == '__main__':
    data = open('prog1.st').read()
    lexer = Lexer()
    lexer.test(data)
    parser = Parser(lexer, debug=True)
    a = parser.parse(data)
    flatten_lists(a)
    t = TemplateEngine(a)
