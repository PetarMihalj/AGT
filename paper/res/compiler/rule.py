class BinaryExpression(ParserRule):
    """BinaryExpression : Expression ADD Expression
                        | Expression SUB Expression
                        | Expression MUL Expression
                        | Expression DIV Expression
                        | Expression MOD Expression
                        | Expression LE Expression
                        | Expression GE Expression
                        | Expression LT Expression
                        | Expression GT Expression
                        | Expression EQ Expression
                        | Expression NE Expression
                        | Expression AND Expression
                        | Expression OR Expression
    """

    def __init__(self, r):
        self.left = r[0]
        self.op = r[1]
        self.right = r[2]
