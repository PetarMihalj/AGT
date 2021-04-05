
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'CompilationUnitleftPLUSMINUSleftTIMESDIVIDEMODleftLEQGEQLTGTEQNEAMPERSAND ARROW ASSIGNMENT BOOLL BREAK COMMA DIVIDE DOT ELSE EQ FN FOR GEQ GT ID IF INTL LBRACE LBRACKET LEQ LET LPAREN LT MINUS MOD NE PLUS RBRACE RBRACKET RETURN RPAREN SEMICOLON SPEC STRUCT TIMES WHILEAddressExpression : AMPERSAND ExpressionArgument : ExpressionArgumentListR : Argument COMMA ArgumentListR\n                     | Argument\n                     | empty\n    AssignmentStatement : Expression ASSIGNMENT Expression SEMICOLON\n                           | Expression ASSIGNMENT Expression\n    BinaryExpression : Expression PLUS Expression\n                        | Expression MINUS Expression\n                        | Expression TIMES Expression\n                        | Expression DIVIDE Expression\n                        | Expression MOD Expression\n                        | Expression LEQ Expression\n                        | Expression GEQ Expression\n                        | Expression LT Expression\n                        | Expression GT Expression\n                        | Expression EQ Expression\n                        | Expression NE Expression\n    BlankStatement : SEMICOLONBlock : LBRACE StatementListR RBRACEBlockStatement : BlockBoolLiteral : BOOLLBracketCall : Expression LBRACKET Expression RBRACKETBreakStatement : BREAK INTL SEMICOLON\n                      | BREAK SEMICOLON\n    CompilationUnit : DefinitionListRDefinitionListR : FunctionDefinition DefinitionListR\n                       | StructDefinition DefinitionListR\n                       | empty\n    DereferenceExpression : TIMES ExpressionDotExpression : ID\n                     | Expression DOT ID\n    Expression : BinaryExpression\n                  | UnaryExpression\n    ForStatement : FOR LPAREN Statement Expression            SEMICOLON Statement RPAREN Block\n    FunctionCall : ID LPAREN ArgumentListR RPAREN\n                    | ID LT TypeArgumentListR GT LPAREN ArgumentListR RPAREN\n    FunctionDefinition : FN ID LPAREN ParameterListR RPAREN Block\n                          | FN ID LT TypeParameterListR GT LPAREN                                  ParameterListR RPAREN Block\n                          | FN ID LPAREN ParameterListR RPAREN                                  ARROW TypeIdentifier Block\n                          | FN ID LT TypeParameterListR GT LPAREN                                  ParameterListR RPAREN                                   ARROW TypeIdentifier Block\n    IfElseStatement : IF LPAREN Expression RPAREN Block ELSE Block\n                       | IF LPAREN Expression RPAREN Block\n    InitCall : ID LBRACE ArgumentListR RBRACE\n                | LT TypeIdentifier GT LBRACE ArgumentListR RBRACE\n                | ID LT TypeArgumentListR GT LBRACE ArgumentListR RBRACEInitStatement : LET ID ASSIGNMENT Expression SEMICOLON\n    IntLiteral : INTLLiteral : IntLiteral\n               | BoolLiteral\n    Parameter : TypeIdentifier IDParameterListR : Parameter COMMA ParameterListR\n                      | Parameter\n                      | empty\n    ReturnStatement : RETURN Expression SEMICOLON\n                       | RETURN SEMICOLON\n    Statement : AssignmentStatement\n                 | InitStatement\n                 | Expression SEMICOLON\n                 | IfElseStatement\n                 | ForStatement\n                 | WhileStatement\n                 | BreakStatement\n                 | ReturnStatement\n                 | BlockStatement\n                 | BlankStatement\n    StatementListR : Statement StatementListR\n                      | empty\n    StructDefinition : STRUCT ID LBRACE StructMemberListR RBRACE\n                        | STRUCT ID LT TypeParameterListR GT                                LBRACE StructMemberListR RBRACE\n    StructMember : TypeIdentifier ID SEMICOLONStructMemberListR : StructMember StructMemberListR\n                         | empty\n    TypeArgumentListR : TypeIdentifier COMMA TypeArgumentListR\n                         | TypeIdentifier\n                         | empty\n    TypeIdentifier : ID\n                      | TypeIdentifier DOT ID\n                      | TypeIdentifier TIMES\n                      | TypeIdentifier LT TypeArgumentListR GTTypeParameter : TypeIdentifier\n                     | ID ASSIGNMENT TypeIdentifier\n                     | SPEC ID ASSIGNMENT TypeIdentifier\n    TypeParameterListR : TypeParameter COMMA TypeParameterListR\n                          | TypeParameter\n                          | empty\n    UnaryExpression : Literal\n                       | FunctionCall\n                       | BracketCall\n                       | InitCall\n                       | DotExpression\n                       | LPAREN Expression RPAREN\n                       | DereferenceExpression\n                       | AddressExpression\n    WhileStatement : WHILE LPAREN Expression RPAREN Block\n    empty :'
    
_lr_action_items = {'FN':([0,3,4,42,46,105,106,140,169,191,],[6,6,6,-69,-38,-40,-20,-70,-39,-41,]),'STRUCT':([0,3,4,42,46,105,106,140,169,191,],[7,7,7,-69,-38,-40,-20,-70,-39,-41,]),'$end':([0,1,2,3,4,5,8,9,42,46,105,106,140,169,191,],[-96,0,-26,-96,-96,-29,-27,-28,-69,-38,-40,-20,-70,-39,-41,]),'ID':([6,7,12,13,14,15,16,18,26,28,30,34,35,36,37,38,40,47,48,49,55,57,58,59,62,64,65,67,68,69,70,71,72,73,74,75,76,77,78,80,81,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,106,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,124,125,126,127,129,130,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,155,163,164,166,167,170,171,172,174,175,177,181,183,185,186,187,188,189,196,197,198,199,201,],[10,11,16,21,16,21,-77,33,41,16,44,49,-79,16,16,16,21,16,76,-78,16,16,-71,16,76,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,123,-31,-33,-34,76,-21,-48,76,76,16,-87,-88,-89,-90,-91,-93,-94,-49,-50,76,-22,16,-80,-20,-59,76,76,76,76,76,76,76,76,76,76,76,76,76,154,76,16,76,76,76,76,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,76,-92,76,-24,-55,16,-6,-23,-36,76,-44,76,-47,76,76,-43,76,-95,-45,-37,-46,-42,-35,]),'LPAREN':([10,39,48,62,64,65,67,68,69,70,71,72,73,74,76,77,78,79,80,81,82,83,85,86,87,89,90,91,92,93,94,95,96,97,98,99,106,108,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,155,163,164,166,167,171,172,174,175,176,177,181,183,185,186,187,188,189,196,197,198,199,201,],[12,55,80,80,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,124,-33,-34,127,80,-21,129,130,-48,80,80,-87,-88,-89,-90,-91,-93,-94,-49,-50,80,-22,-20,-59,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,80,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,80,-92,80,-24,-55,-6,-23,-36,80,185,-44,80,-47,80,80,-43,80,-95,-45,-37,-46,-42,-35,]),'LT':([10,11,16,18,21,23,30,35,48,49,50,54,60,62,64,65,66,67,68,69,70,71,72,73,74,76,77,78,80,81,85,86,87,89,90,91,92,93,94,95,96,97,98,99,101,103,106,108,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,128,129,130,132,133,134,135,136,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,159,162,163,164,165,166,167,171,172,173,174,175,177,179,181,182,183,185,186,187,188,189,196,197,198,199,201,],[13,15,-77,36,-77,36,36,-79,88,-78,36,36,36,88,-57,-58,117,-19,-60,-61,-62,-63,-64,-65,-66,125,-33,-34,88,-21,-48,88,88,-87,-88,-89,-90,-91,-93,-94,-49,-50,88,-22,-80,36,-20,-59,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,117,88,88,-25,117,-56,117,36,117,117,117,117,117,117,117,-13,-14,-15,-16,-17,-18,117,-32,88,117,117,-92,88,117,-24,-55,-6,-23,117,-36,88,-44,117,88,36,-47,88,88,-43,88,-95,-45,-37,-46,-42,-35,]),'LBRACE':([11,16,32,35,45,48,49,60,62,64,65,67,68,69,70,71,72,73,74,76,77,78,81,85,89,90,91,92,93,94,95,96,97,99,101,106,108,129,132,134,135,137,139,141,142,143,144,145,146,147,148,149,150,151,152,154,163,166,167,168,171,172,174,176,177,178,180,182,183,187,188,189,194,196,197,198,199,200,201,],[14,-77,48,-79,59,48,-78,48,48,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,126,-33,-34,-21,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,-80,-20,-59,48,-25,-56,-30,-1,48,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,-92,-24,-55,181,-6,-23,-36,186,-44,48,48,48,-47,-43,48,-95,48,-45,-37,-46,-42,48,-35,]),'RPAREN':([12,17,19,20,33,37,53,55,64,65,67,68,69,70,71,72,73,74,76,77,78,81,85,89,90,91,92,93,94,95,96,97,99,102,106,108,124,128,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,156,157,158,159,162,163,165,166,167,171,172,174,175,177,183,184,185,187,189,192,195,196,197,198,199,201,],[-96,32,-53,-54,-51,-96,-52,-96,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,-21,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,139,-20,-59,-96,163,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,174,-4,-5,-2,178,-92,180,-24,-55,-6,-23,-36,-96,-44,-47,-3,-96,-43,-95,197,200,-45,-37,-46,-42,-35,]),'SPEC':([13,15,40,],[26,26,26,]),'GT':([13,15,16,21,22,23,24,25,31,35,36,40,49,50,51,52,54,56,66,76,77,78,85,89,90,91,92,93,94,95,96,97,99,100,101,103,125,128,133,135,136,137,138,141,142,143,144,145,146,147,148,149,150,151,152,153,154,159,160,162,163,165,172,173,174,177,179,196,197,198,],[-96,-96,-77,-77,39,-81,-85,-86,45,-79,-96,-96,-78,-75,101,-76,-82,-84,118,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,-96,-80,-83,-96,118,118,118,168,118,-74,118,118,118,118,118,118,-13,-14,-15,-16,-17,-18,118,-32,118,176,118,-92,118,-23,118,-36,-44,118,-45,-37,-46,]),'RBRACE':([14,27,28,29,43,48,58,59,61,62,63,64,65,67,68,69,70,71,72,73,74,76,77,78,81,85,89,90,91,92,93,94,95,96,97,99,104,106,107,108,126,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,157,158,159,161,163,166,167,171,172,174,175,177,181,183,184,186,187,189,190,193,196,197,198,199,201,],[-96,42,-96,-73,-72,-96,-71,-96,106,-96,-68,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,-21,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,140,-20,-67,-59,-96,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,-4,-5,-2,177,-92,-24,-55,-6,-23,-36,-96,-44,-96,-47,-3,-96,-43,-95,196,198,-45,-37,-46,-42,-35,]),'DOT':([16,18,21,23,30,35,49,50,54,60,66,76,77,78,85,89,90,91,92,93,94,95,96,97,99,101,103,128,133,135,136,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,159,162,163,165,172,173,174,177,179,182,196,197,198,],[-77,34,-77,34,34,-79,-78,34,34,34,122,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,-80,34,122,122,-30,34,122,122,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,122,-32,122,122,-92,122,-23,122,-36,-44,122,34,-45,-37,-46,]),'TIMES':([16,18,21,23,30,35,48,49,50,54,60,62,64,65,66,67,68,69,70,71,72,73,74,76,77,78,80,81,85,86,87,89,90,91,92,93,94,95,96,97,98,99,101,103,106,108,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,128,129,130,132,133,134,135,136,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,159,162,163,164,165,166,167,171,172,173,174,175,177,179,181,182,183,185,186,187,188,189,196,197,198,199,201,],[-77,35,-77,35,35,-79,87,-78,35,35,35,87,-57,-58,112,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,87,-21,-48,87,87,-87,-88,-89,-90,-91,-93,-94,-49,-50,87,-22,-80,35,-20,-59,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,87,112,87,87,-25,112,-56,-30,35,112,112,112,112,-10,-11,-12,-13,-14,-15,-16,-17,-18,112,-32,87,112,112,-92,87,112,-24,-55,-6,-23,112,-36,87,-44,112,87,35,-47,87,87,-43,87,-95,-45,-37,-46,-42,-35,]),'COMMA':([16,19,21,23,24,33,35,49,50,54,76,77,78,85,89,90,91,92,93,94,95,96,97,99,101,103,135,137,142,143,144,145,146,147,148,149,150,151,152,154,157,159,163,172,174,177,196,197,198,],[-77,37,-77,-81,40,-51,-79,-78,100,-82,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,-80,-83,-30,-1,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,175,-2,-92,-23,-36,-44,-45,-37,-46,]),'ASSIGNMENT':([21,41,66,76,77,78,85,89,90,91,92,93,94,95,96,97,99,123,135,137,142,143,144,145,146,147,148,149,150,151,152,154,163,172,174,177,196,197,198,],[38,57,109,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,155,-30,-1,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,-92,-23,-36,-44,-45,-37,-46,]),'ARROW':([32,139,],[47,170,]),'SEMICOLON':([44,48,62,64,65,66,67,68,69,70,71,72,73,74,76,77,78,81,84,85,86,89,90,91,92,93,94,95,96,97,99,106,108,129,131,132,133,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,163,166,167,171,172,173,174,177,179,183,187,188,189,196,197,198,199,201,],[58,67,67,-57,-58,108,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,-21,132,-48,134,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,-20,-59,67,166,-25,167,-56,-30,-1,171,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,-92,-24,-55,-6,-23,183,-36,-44,188,-47,-43,67,-95,-45,-37,-46,-42,-35,]),'LET':([48,62,64,65,67,68,69,70,71,72,73,74,76,77,78,81,85,89,90,91,92,93,94,95,96,97,99,106,108,129,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,163,166,167,171,172,174,177,183,187,188,189,196,197,198,199,201,],[75,75,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,-21,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,-20,-59,75,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,-92,-24,-55,-6,-23,-36,-44,-47,-43,75,-95,-45,-37,-46,-42,-35,]),'IF':([48,62,64,65,67,68,69,70,71,72,73,74,76,77,78,81,85,89,90,91,92,93,94,95,96,97,99,106,108,129,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,163,166,167,171,172,174,177,183,187,188,189,196,197,198,199,201,],[79,79,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,-21,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,-20,-59,79,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,-92,-24,-55,-6,-23,-36,-44,-47,-43,79,-95,-45,-37,-46,-42,-35,]),'FOR':([48,62,64,65,67,68,69,70,71,72,73,74,76,77,78,81,85,89,90,91,92,93,94,95,96,97,99,106,108,129,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,163,166,167,171,172,174,177,183,187,188,189,196,197,198,199,201,],[82,82,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,-21,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,-20,-59,82,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,-92,-24,-55,-6,-23,-36,-44,-47,-43,82,-95,-45,-37,-46,-42,-35,]),'WHILE':([48,62,64,65,67,68,69,70,71,72,73,74,76,77,78,81,85,89,90,91,92,93,94,95,96,97,99,106,108,129,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,163,166,167,171,172,174,177,183,187,188,189,196,197,198,199,201,],[83,83,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,-21,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,-20,-59,83,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,-92,-24,-55,-6,-23,-36,-44,-47,-43,83,-95,-45,-37,-46,-42,-35,]),'BREAK':([48,62,64,65,67,68,69,70,71,72,73,74,76,77,78,81,85,89,90,91,92,93,94,95,96,97,99,106,108,129,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,163,166,167,171,172,174,177,183,187,188,189,196,197,198,199,201,],[84,84,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,-21,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,-20,-59,84,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,-92,-24,-55,-6,-23,-36,-44,-47,-43,84,-95,-45,-37,-46,-42,-35,]),'RETURN':([48,62,64,65,67,68,69,70,71,72,73,74,76,77,78,81,85,89,90,91,92,93,94,95,96,97,99,106,108,129,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,163,166,167,171,172,174,177,183,187,188,189,196,197,198,199,201,],[86,86,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,-21,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,-20,-59,86,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,-92,-24,-55,-6,-23,-36,-44,-47,-43,86,-95,-45,-37,-46,-42,-35,]),'AMPERSAND':([48,62,64,65,67,68,69,70,71,72,73,74,76,77,78,80,81,85,86,87,89,90,91,92,93,94,95,96,97,98,99,106,108,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,155,163,164,166,167,171,172,174,175,177,181,183,185,186,187,188,189,196,197,198,199,201,],[98,98,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,98,-21,-48,98,98,-87,-88,-89,-90,-91,-93,-94,-49,-50,98,-22,-20,-59,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,98,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,98,-92,98,-24,-55,-6,-23,-36,98,-44,98,-47,98,98,-43,98,-95,-45,-37,-46,-42,-35,]),'INTL':([48,62,64,65,67,68,69,70,71,72,73,74,76,77,78,80,81,84,85,86,87,89,90,91,92,93,94,95,96,97,98,99,106,108,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,155,163,164,166,167,171,172,174,175,177,181,183,185,186,187,188,189,196,197,198,199,201,],[85,85,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,85,-21,131,-48,85,85,-87,-88,-89,-90,-91,-93,-94,-49,-50,85,-22,-20,-59,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,85,-92,85,-24,-55,-6,-23,-36,85,-44,85,-47,85,85,-43,85,-95,-45,-37,-46,-42,-35,]),'BOOLL':([48,62,64,65,67,68,69,70,71,72,73,74,76,77,78,80,81,85,86,87,89,90,91,92,93,94,95,96,97,98,99,106,108,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,132,134,135,137,141,142,143,144,145,146,147,148,149,150,151,152,154,155,163,164,166,167,171,172,174,175,177,181,183,185,186,187,188,189,196,197,198,199,201,],[99,99,-57,-58,-19,-60,-61,-62,-63,-64,-65,-66,-31,-33,-34,99,-21,-48,99,99,-87,-88,-89,-90,-91,-93,-94,-49,-50,99,-22,-20,-59,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,99,-25,-56,-30,-1,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-32,99,-92,99,-24,-55,-6,-23,-36,99,-44,99,-47,99,99,-43,99,-95,-45,-37,-46,-42,-35,]),'PLUS':([66,76,77,78,85,89,90,91,92,93,94,95,96,97,99,128,133,135,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,159,162,163,165,172,173,174,177,179,196,197,198,],[110,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,110,110,-30,110,110,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,110,-32,110,110,-92,110,-23,110,-36,-44,110,-45,-37,-46,]),'MINUS':([66,76,77,78,85,89,90,91,92,93,94,95,96,97,99,128,133,135,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,159,162,163,165,172,173,174,177,179,196,197,198,],[111,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,111,111,-30,111,111,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,111,-32,111,111,-92,111,-23,111,-36,-44,111,-45,-37,-46,]),'DIVIDE':([66,76,77,78,85,89,90,91,92,93,94,95,96,97,99,128,133,135,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,159,162,163,165,172,173,174,177,179,196,197,198,],[113,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,113,113,-30,113,113,113,113,-10,-11,-12,-13,-14,-15,-16,-17,-18,113,-32,113,113,-92,113,-23,113,-36,-44,113,-45,-37,-46,]),'MOD':([66,76,77,78,85,89,90,91,92,93,94,95,96,97,99,128,133,135,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,159,162,163,165,172,173,174,177,179,196,197,198,],[114,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,114,114,-30,114,114,114,114,-10,-11,-12,-13,-14,-15,-16,-17,-18,114,-32,114,114,-92,114,-23,114,-36,-44,114,-45,-37,-46,]),'LEQ':([66,76,77,78,85,89,90,91,92,93,94,95,96,97,99,128,133,135,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,159,162,163,165,172,173,174,177,179,196,197,198,],[115,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,115,115,115,115,115,115,115,115,115,115,-13,-14,-15,-16,-17,-18,115,-32,115,115,-92,115,-23,115,-36,-44,115,-45,-37,-46,]),'GEQ':([66,76,77,78,85,89,90,91,92,93,94,95,96,97,99,128,133,135,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,159,162,163,165,172,173,174,177,179,196,197,198,],[116,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,116,116,116,116,116,116,116,116,116,116,-13,-14,-15,-16,-17,-18,116,-32,116,116,-92,116,-23,116,-36,-44,116,-45,-37,-46,]),'EQ':([66,76,77,78,85,89,90,91,92,93,94,95,96,97,99,128,133,135,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,159,162,163,165,172,173,174,177,179,196,197,198,],[119,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,119,119,119,119,119,119,119,119,119,119,-13,-14,-15,-16,-17,-18,119,-32,119,119,-92,119,-23,119,-36,-44,119,-45,-37,-46,]),'NE':([66,76,77,78,85,89,90,91,92,93,94,95,96,97,99,128,133,135,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,159,162,163,165,172,173,174,177,179,196,197,198,],[120,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,120,120,120,120,120,120,120,120,120,120,-13,-14,-15,-16,-17,-18,120,-32,120,120,-92,120,-23,120,-36,-44,120,-45,-37,-46,]),'LBRACKET':([66,76,77,78,85,89,90,91,92,93,94,95,96,97,99,128,133,135,137,141,142,143,144,145,146,147,148,149,150,151,152,153,154,159,162,163,165,172,173,174,177,179,196,197,198,],[121,-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,121,121,-30,121,121,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,121,-32,121,121,-92,121,-23,121,-36,-44,121,-45,-37,-46,]),'RBRACKET':([76,77,78,85,89,90,91,92,93,94,95,96,97,99,135,137,142,143,144,145,146,147,148,149,150,151,152,153,154,163,172,174,177,196,197,198,],[-31,-33,-34,-48,-87,-88,-89,-90,-91,-93,-94,-49,-50,-22,-30,-1,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,172,-32,-92,-23,-36,-44,-45,-37,-46,]),'ELSE':([106,187,],[-20,194,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'CompilationUnit':([0,],[1,]),'DefinitionListR':([0,3,4,],[2,8,9,]),'FunctionDefinition':([0,3,4,],[3,3,3,]),'StructDefinition':([0,3,4,],[4,4,4,]),'empty':([0,3,4,12,13,14,15,28,36,37,40,48,55,59,62,100,124,125,126,175,181,185,186,],[5,5,5,20,25,29,25,29,52,20,25,63,20,29,63,52,158,52,158,158,158,158,158,]),'ParameterListR':([12,37,55,],[17,53,102,]),'TypeIdentifier':([12,13,14,15,28,36,37,38,40,47,55,57,59,88,100,125,170,],[18,23,30,23,30,50,18,54,23,60,18,103,30,136,50,50,182,]),'Parameter':([12,37,55,],[19,19,19,]),'TypeParameterListR':([13,15,40,],[22,31,56,]),'TypeParameter':([13,15,40,],[24,24,24,]),'StructMemberListR':([14,28,59,],[27,43,104,]),'StructMember':([14,28,59,],[28,28,28,]),'Block':([32,48,60,62,129,139,178,180,182,188,194,200,],[46,81,105,81,81,169,187,189,191,81,199,201,]),'TypeArgumentListR':([36,100,125,],[51,138,160,]),'StatementListR':([48,62,],[61,107,]),'Statement':([48,62,129,188,],[62,62,164,195,]),'AssignmentStatement':([48,62,129,188,],[64,64,64,64,]),'InitStatement':([48,62,129,188,],[65,65,65,65,]),'Expression':([48,62,80,86,87,98,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,155,164,175,181,185,186,188,],[66,66,128,133,135,137,141,142,143,144,145,146,147,148,149,150,151,152,153,159,159,162,66,165,173,179,159,159,159,159,66,]),'IfElseStatement':([48,62,129,188,],[68,68,68,68,]),'ForStatement':([48,62,129,188,],[69,69,69,69,]),'WhileStatement':([48,62,129,188,],[70,70,70,70,]),'BreakStatement':([48,62,129,188,],[71,71,71,71,]),'ReturnStatement':([48,62,129,188,],[72,72,72,72,]),'BlockStatement':([48,62,129,188,],[73,73,73,73,]),'BlankStatement':([48,62,129,188,],[74,74,74,74,]),'BinaryExpression':([48,62,80,86,87,98,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,155,164,175,181,185,186,188,],[77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,77,]),'UnaryExpression':([48,62,80,86,87,98,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,155,164,175,181,185,186,188,],[78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,78,]),'Literal':([48,62,80,86,87,98,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,155,164,175,181,185,186,188,],[89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,]),'FunctionCall':([48,62,80,86,87,98,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,155,164,175,181,185,186,188,],[90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,90,]),'BracketCall':([48,62,80,86,87,98,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,155,164,175,181,185,186,188,],[91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,]),'InitCall':([48,62,80,86,87,98,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,155,164,175,181,185,186,188,],[92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,92,]),'DotExpression':([48,62,80,86,87,98,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,155,164,175,181,185,186,188,],[93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,93,]),'DereferenceExpression':([48,62,80,86,87,98,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,155,164,175,181,185,186,188,],[94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,94,]),'AddressExpression':([48,62,80,86,87,98,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,155,164,175,181,185,186,188,],[95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,95,]),'IntLiteral':([48,62,80,86,87,98,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,155,164,175,181,185,186,188,],[96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,]),'BoolLiteral':([48,62,80,86,87,98,109,110,111,112,113,114,115,116,117,118,119,120,121,124,126,127,129,130,155,164,175,181,185,186,188,],[97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,97,]),'ArgumentListR':([124,126,175,181,185,186,],[156,161,184,190,192,193,]),'Argument':([124,126,175,181,185,186,],[157,157,157,157,157,157,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> CompilationUnit","S'",1,None,None,None),
  ('AddressExpression -> AMPERSAND Expression','AddressExpression',2,"p_<class 'parser_rules.AddressExpression'>",'parser.py',28),
  ('Argument -> Expression','Argument',1,"p_<class 'parser_rules.Argument'>",'parser.py',28),
  ('ArgumentListR -> Argument COMMA ArgumentListR','ArgumentListR',3,"p_<class 'parser_rules.ArgumentListR'>",'parser.py',28),
  ('ArgumentListR -> Argument','ArgumentListR',1,"p_<class 'parser_rules.ArgumentListR'>",'parser.py',29),
  ('ArgumentListR -> empty','ArgumentListR',1,"p_<class 'parser_rules.ArgumentListR'>",'parser.py',30),
  ('AssignmentStatement -> Expression ASSIGNMENT Expression SEMICOLON','AssignmentStatement',4,"p_<class 'parser_rules.AssignmentStatement'>",'parser.py',28),
  ('AssignmentStatement -> Expression ASSIGNMENT Expression','AssignmentStatement',3,"p_<class 'parser_rules.AssignmentStatement'>",'parser.py',29),
  ('BinaryExpression -> Expression PLUS Expression','BinaryExpression',3,"p_<class 'parser_rules.BinaryExpression'>",'parser.py',28),
  ('BinaryExpression -> Expression MINUS Expression','BinaryExpression',3,"p_<class 'parser_rules.BinaryExpression'>",'parser.py',29),
  ('BinaryExpression -> Expression TIMES Expression','BinaryExpression',3,"p_<class 'parser_rules.BinaryExpression'>",'parser.py',30),
  ('BinaryExpression -> Expression DIVIDE Expression','BinaryExpression',3,"p_<class 'parser_rules.BinaryExpression'>",'parser.py',31),
  ('BinaryExpression -> Expression MOD Expression','BinaryExpression',3,"p_<class 'parser_rules.BinaryExpression'>",'parser.py',32),
  ('BinaryExpression -> Expression LEQ Expression','BinaryExpression',3,"p_<class 'parser_rules.BinaryExpression'>",'parser.py',33),
  ('BinaryExpression -> Expression GEQ Expression','BinaryExpression',3,"p_<class 'parser_rules.BinaryExpression'>",'parser.py',34),
  ('BinaryExpression -> Expression LT Expression','BinaryExpression',3,"p_<class 'parser_rules.BinaryExpression'>",'parser.py',35),
  ('BinaryExpression -> Expression GT Expression','BinaryExpression',3,"p_<class 'parser_rules.BinaryExpression'>",'parser.py',36),
  ('BinaryExpression -> Expression EQ Expression','BinaryExpression',3,"p_<class 'parser_rules.BinaryExpression'>",'parser.py',37),
  ('BinaryExpression -> Expression NE Expression','BinaryExpression',3,"p_<class 'parser_rules.BinaryExpression'>",'parser.py',38),
  ('BlankStatement -> SEMICOLON','BlankStatement',1,"p_<class 'parser_rules.BlankStatement'>",'parser.py',28),
  ('Block -> LBRACE StatementListR RBRACE','Block',3,"p_<class 'parser_rules.Block'>",'parser.py',28),
  ('BlockStatement -> Block','BlockStatement',1,"p_<class 'parser_rules.BlockStatement'>",'parser.py',28),
  ('BoolLiteral -> BOOLL','BoolLiteral',1,"p_<class 'parser_rules.BoolLiteral'>",'parser.py',28),
  ('BracketCall -> Expression LBRACKET Expression RBRACKET','BracketCall',4,"p_<class 'parser_rules.BracketCall'>",'parser.py',28),
  ('BreakStatement -> BREAK INTL SEMICOLON','BreakStatement',3,"p_<class 'parser_rules.BreakStatement'>",'parser.py',28),
  ('BreakStatement -> BREAK SEMICOLON','BreakStatement',2,"p_<class 'parser_rules.BreakStatement'>",'parser.py',29),
  ('CompilationUnit -> DefinitionListR','CompilationUnit',1,"p_<class 'parser_rules.CompilationUnit'>",'parser.py',28),
  ('DefinitionListR -> FunctionDefinition DefinitionListR','DefinitionListR',2,"p_<class 'parser_rules.DefinitionListR'>",'parser.py',28),
  ('DefinitionListR -> StructDefinition DefinitionListR','DefinitionListR',2,"p_<class 'parser_rules.DefinitionListR'>",'parser.py',29),
  ('DefinitionListR -> empty','DefinitionListR',1,"p_<class 'parser_rules.DefinitionListR'>",'parser.py',30),
  ('DereferenceExpression -> TIMES Expression','DereferenceExpression',2,"p_<class 'parser_rules.DereferenceExpression'>",'parser.py',28),
  ('DotExpression -> ID','DotExpression',1,"p_<class 'parser_rules.DotExpression'>",'parser.py',28),
  ('DotExpression -> Expression DOT ID','DotExpression',3,"p_<class 'parser_rules.DotExpression'>",'parser.py',29),
  ('Expression -> BinaryExpression','Expression',1,"p_<class 'parser_rules.Expression'>",'parser.py',28),
  ('Expression -> UnaryExpression','Expression',1,"p_<class 'parser_rules.Expression'>",'parser.py',29),
  ('ForStatement -> FOR LPAREN Statement Expression SEMICOLON Statement RPAREN Block','ForStatement',8,"p_<class 'parser_rules.ForStatement'>",'parser.py',28),
  ('FunctionCall -> ID LPAREN ArgumentListR RPAREN','FunctionCall',4,"p_<class 'parser_rules.FunctionCall'>",'parser.py',28),
  ('FunctionCall -> ID LT TypeArgumentListR GT LPAREN ArgumentListR RPAREN','FunctionCall',7,"p_<class 'parser_rules.FunctionCall'>",'parser.py',29),
  ('FunctionDefinition -> FN ID LPAREN ParameterListR RPAREN Block','FunctionDefinition',6,"p_<class 'parser_rules.FunctionDefinition'>",'parser.py',28),
  ('FunctionDefinition -> FN ID LT TypeParameterListR GT LPAREN ParameterListR RPAREN Block','FunctionDefinition',9,"p_<class 'parser_rules.FunctionDefinition'>",'parser.py',29),
  ('FunctionDefinition -> FN ID LPAREN ParameterListR RPAREN ARROW TypeIdentifier Block','FunctionDefinition',8,"p_<class 'parser_rules.FunctionDefinition'>",'parser.py',30),
  ('FunctionDefinition -> FN ID LT TypeParameterListR GT LPAREN ParameterListR RPAREN ARROW TypeIdentifier Block','FunctionDefinition',11,"p_<class 'parser_rules.FunctionDefinition'>",'parser.py',31),
  ('IfElseStatement -> IF LPAREN Expression RPAREN Block ELSE Block','IfElseStatement',7,"p_<class 'parser_rules.IfElseStatement'>",'parser.py',28),
  ('IfElseStatement -> IF LPAREN Expression RPAREN Block','IfElseStatement',5,"p_<class 'parser_rules.IfElseStatement'>",'parser.py',29),
  ('InitCall -> ID LBRACE ArgumentListR RBRACE','InitCall',4,"p_<class 'parser_rules.InitCall'>",'parser.py',28),
  ('InitCall -> LT TypeIdentifier GT LBRACE ArgumentListR RBRACE','InitCall',6,"p_<class 'parser_rules.InitCall'>",'parser.py',29),
  ('InitCall -> ID LT TypeArgumentListR GT LBRACE ArgumentListR RBRACE','InitCall',7,"p_<class 'parser_rules.InitCall'>",'parser.py',30),
  ('InitStatement -> LET ID ASSIGNMENT Expression SEMICOLON','InitStatement',5,"p_<class 'parser_rules.InitStatement'>",'parser.py',28),
  ('IntLiteral -> INTL','IntLiteral',1,"p_<class 'parser_rules.IntLiteral'>",'parser.py',28),
  ('Literal -> IntLiteral','Literal',1,"p_<class 'parser_rules.Literal'>",'parser.py',28),
  ('Literal -> BoolLiteral','Literal',1,"p_<class 'parser_rules.Literal'>",'parser.py',29),
  ('Parameter -> TypeIdentifier ID','Parameter',2,"p_<class 'parser_rules.Parameter'>",'parser.py',28),
  ('ParameterListR -> Parameter COMMA ParameterListR','ParameterListR',3,"p_<class 'parser_rules.ParameterListR'>",'parser.py',28),
  ('ParameterListR -> Parameter','ParameterListR',1,"p_<class 'parser_rules.ParameterListR'>",'parser.py',29),
  ('ParameterListR -> empty','ParameterListR',1,"p_<class 'parser_rules.ParameterListR'>",'parser.py',30),
  ('ReturnStatement -> RETURN Expression SEMICOLON','ReturnStatement',3,"p_<class 'parser_rules.ReturnStatement'>",'parser.py',28),
  ('ReturnStatement -> RETURN SEMICOLON','ReturnStatement',2,"p_<class 'parser_rules.ReturnStatement'>",'parser.py',29),
  ('Statement -> AssignmentStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',28),
  ('Statement -> InitStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',29),
  ('Statement -> Expression SEMICOLON','Statement',2,"p_<class 'parser_rules.Statement'>",'parser.py',30),
  ('Statement -> IfElseStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',31),
  ('Statement -> ForStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',32),
  ('Statement -> WhileStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',33),
  ('Statement -> BreakStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',34),
  ('Statement -> ReturnStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',35),
  ('Statement -> BlockStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',36),
  ('Statement -> BlankStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',37),
  ('StatementListR -> Statement StatementListR','StatementListR',2,"p_<class 'parser_rules.StatementListR'>",'parser.py',28),
  ('StatementListR -> empty','StatementListR',1,"p_<class 'parser_rules.StatementListR'>",'parser.py',29),
  ('StructDefinition -> STRUCT ID LBRACE StructMemberListR RBRACE','StructDefinition',5,"p_<class 'parser_rules.StructDefinition'>",'parser.py',28),
  ('StructDefinition -> STRUCT ID LT TypeParameterListR GT LBRACE StructMemberListR RBRACE','StructDefinition',8,"p_<class 'parser_rules.StructDefinition'>",'parser.py',29),
  ('StructMember -> TypeIdentifier ID SEMICOLON','StructMember',3,"p_<class 'parser_rules.StructMember'>",'parser.py',28),
  ('StructMemberListR -> StructMember StructMemberListR','StructMemberListR',2,"p_<class 'parser_rules.StructMemberListR'>",'parser.py',28),
  ('StructMemberListR -> empty','StructMemberListR',1,"p_<class 'parser_rules.StructMemberListR'>",'parser.py',29),
  ('TypeArgumentListR -> TypeIdentifier COMMA TypeArgumentListR','TypeArgumentListR',3,"p_<class 'parser_rules.TypeArgumentListR'>",'parser.py',28),
  ('TypeArgumentListR -> TypeIdentifier','TypeArgumentListR',1,"p_<class 'parser_rules.TypeArgumentListR'>",'parser.py',29),
  ('TypeArgumentListR -> empty','TypeArgumentListR',1,"p_<class 'parser_rules.TypeArgumentListR'>",'parser.py',30),
  ('TypeIdentifier -> ID','TypeIdentifier',1,"p_<class 'parser_rules.TypeIdentifier'>",'parser.py',28),
  ('TypeIdentifier -> TypeIdentifier DOT ID','TypeIdentifier',3,"p_<class 'parser_rules.TypeIdentifier'>",'parser.py',29),
  ('TypeIdentifier -> TypeIdentifier TIMES','TypeIdentifier',2,"p_<class 'parser_rules.TypeIdentifier'>",'parser.py',30),
  ('TypeIdentifier -> TypeIdentifier LT TypeArgumentListR GT','TypeIdentifier',4,"p_<class 'parser_rules.TypeIdentifier'>",'parser.py',31),
  ('TypeParameter -> TypeIdentifier','TypeParameter',1,"p_<class 'parser_rules.TypeParameter'>",'parser.py',28),
  ('TypeParameter -> ID ASSIGNMENT TypeIdentifier','TypeParameter',3,"p_<class 'parser_rules.TypeParameter'>",'parser.py',29),
  ('TypeParameter -> SPEC ID ASSIGNMENT TypeIdentifier','TypeParameter',4,"p_<class 'parser_rules.TypeParameter'>",'parser.py',30),
  ('TypeParameterListR -> TypeParameter COMMA TypeParameterListR','TypeParameterListR',3,"p_<class 'parser_rules.TypeParameterListR'>",'parser.py',28),
  ('TypeParameterListR -> TypeParameter','TypeParameterListR',1,"p_<class 'parser_rules.TypeParameterListR'>",'parser.py',29),
  ('TypeParameterListR -> empty','TypeParameterListR',1,"p_<class 'parser_rules.TypeParameterListR'>",'parser.py',30),
  ('UnaryExpression -> Literal','UnaryExpression',1,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',28),
  ('UnaryExpression -> FunctionCall','UnaryExpression',1,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',29),
  ('UnaryExpression -> BracketCall','UnaryExpression',1,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',30),
  ('UnaryExpression -> InitCall','UnaryExpression',1,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',31),
  ('UnaryExpression -> DotExpression','UnaryExpression',1,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',32),
  ('UnaryExpression -> LPAREN Expression RPAREN','UnaryExpression',3,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',33),
  ('UnaryExpression -> DereferenceExpression','UnaryExpression',1,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',34),
  ('UnaryExpression -> AddressExpression','UnaryExpression',1,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',35),
  ('WhileStatement -> WHILE LPAREN Expression RPAREN Block','WhileStatement',5,"p_<class 'parser_rules.WhileStatement'>",'parser.py',28),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',35),
]
