
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "CompilationUnitleftPLUSMINUSleftTIMESDIVIDEMODleftLEQGEQLTGTEQNEAMPERSAND ASSIGNMENT BOOLL BREAK COMMA DIVIDE DOT ELSE EQ FOR GEQ GT ID IF INTL LBRACE LBRACKET LEQ LPAREN LT MINUS MOD NE PLUS RBRACE RBRACKET RETURN RPAREN SEMICOLON STRUCT TIMES WHILEArgument : ExpressionArgumentListR : Argument COMMA ArgumentListR\n                     | Argument\n                     | empty\n    AssignmentStatement : Expression ASSIGNMENT Expression SEMICOLON\n                           | Expression ASSIGNMENT Expression\n    BinaryExpression : Expression PLUS Expression\n                        | Expression MINUS Expression\n                        | Expression TIMES Expression\n                        | Expression DIVIDE Expression\n                        | Expression MOD Expression\n                        | Expression LEQ Expression\n                        | Expression GEQ Expression\n                        | Expression LT Expression\n                        | Expression GT Expression\n                        | Expression EQ Expression\n                        | Expression NE Expression\n                        | Expression DOT Expression\n\n    BlankStatement : ';'Block : LBRACE StatementListR RBRACEBlockStatement : BlockBoolLiteral : BOOLLBracketCall : Expression LBRACKET Expression RBRACKETBreakStatement : BREAK INTL SEMICOLON\n                      | BREAK SEMICOLON\n    CompilationUnit : DefinitionListRDeclarationAssignmentStatement : Type Id ASSIGNMENT                                        Expression SEMICOLONDeclarationFunctionCallStatement : Type FunctionCall SEMICOLONDeclarationStatement : Type Id SEMICOLONDefinitionListR : FunctionDefinition DefinitionListR\n                       | StructDefinition DefinitionListR\n                       | empty\n    Expression : BinaryExpression\n                  | UnaryExpression\n    ForStatement : FOR LPAREN Statement Expression            SEMICOLON Statement RPAREN Block\n    FunctionCall : Id LPAREN ArgumentListR RPAREN\n    FunctionDefinition : Type Id LPAREN ParameterListR RPAREN Block\n    Id : IDIfElseStatement : IF LPAREN Expression RPAREN Block ELSE Block\n    IntLiteral : INTLLiteral : IntLiteral\n               | BoolLiteral\n    Parameter : Type IdParameterListR : Parameter COMMA ParameterListR\n                      | Parameter\n                      | empty\n    PointerListR : TIMES PointerListR\n                    | empty\n    ReturnStatement : RETURN Expression SEMICOLON\n                       | RETURN SEMICOLON\n    Statement : AssignmentStatement\n                 | DeclarationAssignmentStatement\n                 | DeclarationFunctionCallStatement\n                 | DeclarationStatement\n                 | Expression SEMICOLON\n                 | IfElseStatement\n                 | ForStatement\n                 | WhileStatement\n                 | BreakStatement\n                 | ReturnStatement\n                 | BlockStatement\n                 | BlankStatement\n    StatementListR : Statement StatementListR\n                      | empty\n    StructDefinition : STRUCT Id            LBRACE StructMemberListR RBRACE\n    StructMember : Type Id SEMICOLONStructMemberListR : StructMember StructMemberListR\n                         | empty\n    Type : Id PointerListRUnaryExpression : Id\n                       | Literal\n                       | FunctionCall\n                       | BracketCall\n                       | LPAREN Expression RPAREN\n                       | TIMES Expression\n                       | AMPERSAND Expression\n    WhileStatement : WHILE LPAREN Expression RPAREN Block\n    empty :"
    
_lr_action_items = {'STRUCT':([0,3,4,31,34,74,],[8,8,8,-65,-37,-20,]),'$end':([0,1,2,3,4,5,10,11,31,34,74,],[-78,0,-26,-78,-78,-32,-30,-31,-65,-37,-20,]),'ID':([0,3,4,6,7,8,9,13,14,15,17,18,19,20,25,27,30,31,34,35,37,39,41,42,43,44,46,47,48,49,50,51,52,53,54,55,56,57,59,60,64,65,66,67,68,69,70,71,72,73,74,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,96,97,98,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,119,120,121,127,128,130,131,132,133,135,136,140,143,144,147,149,],[9,9,9,9,-78,9,-38,-69,-78,-48,9,-47,9,9,9,9,9,-65,-37,9,-66,9,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,9,-78,-72,-33,-34,9,-21,-40,9,-19,9,-71,-73,9,-41,-42,-22,-20,-55,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,-70,9,9,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,9,-29,-28,-74,9,-24,-49,-5,-23,-36,9,-27,9,-77,-39,-35,]),'TIMES':([7,9,14,35,39,41,42,43,44,45,46,47,48,49,50,51,52,54,55,56,57,59,60,64,65,66,67,68,69,70,71,72,73,74,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,95,96,97,98,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,125,126,127,128,129,130,131,132,133,134,135,136,138,140,143,144,147,149,],[14,-38,14,67,67,-51,-52,-53,-54,80,-56,-57,-58,-59,-60,-61,-62,14,-72,-33,-34,67,-21,-40,67,-19,67,-71,-73,67,-41,-42,-22,-20,-55,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,80,-70,67,67,-25,80,-50,-75,80,80,80,80,-9,-10,-11,-12,-13,-14,-15,-16,-17,80,80,67,-29,-28,80,80,-74,67,80,-24,-49,-5,-23,80,-36,67,80,-27,67,-77,-39,-35,]),'LPAREN':([9,12,35,39,41,42,43,44,46,47,48,49,50,51,52,54,55,56,57,58,59,60,61,62,64,65,66,67,68,69,70,71,72,73,74,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,93,94,96,97,98,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,119,120,121,127,128,130,131,132,133,135,136,140,143,144,147,149,],[-38,17,59,59,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,93,-72,-33,-34,94,59,-21,97,98,-40,59,-19,59,-71,-73,59,-41,-42,-22,-20,-55,59,59,59,59,59,59,59,59,59,59,59,59,59,59,93,59,59,93,59,59,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,59,-29,-28,-74,59,-24,-49,-5,-23,-36,59,-27,59,-77,-39,-35,]),'LBRACE':([9,16,29,35,39,41,42,43,44,46,47,48,49,50,51,52,55,56,57,60,64,66,68,69,71,72,73,74,76,96,97,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,120,121,127,130,131,132,133,135,137,139,140,143,144,145,147,148,149,],[-38,19,35,35,35,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,-72,-33,-34,-21,-40,-19,-71,-73,-41,-42,-22,-20,-55,-70,35,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-29,-28,-74,-24,-49,-5,-23,-36,35,35,-27,35,-77,35,-39,35,-35,]),'COMMA':([9,22,28,55,56,57,64,68,69,71,72,73,96,103,104,106,107,108,109,110,111,112,113,114,115,116,117,123,125,127,133,135,],[-38,30,-43,-72,-33,-34,-40,-71,-73,-41,-42,-22,-70,-75,-76,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,136,-1,-74,-23,-36,]),'RPAREN':([9,17,21,22,23,28,30,36,41,42,43,44,46,47,48,49,50,51,52,55,56,57,60,64,66,68,69,71,72,73,74,76,93,95,96,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,120,121,122,123,124,125,126,127,129,130,131,132,133,135,136,140,141,144,146,147,149,],[-38,-78,29,-45,-46,-43,-78,-44,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,-72,-33,-34,-21,-40,-19,-71,-73,-41,-42,-22,-20,-55,-78,127,-70,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-29,-28,135,-3,-4,-1,137,-74,139,-24,-49,-5,-23,-36,-78,-27,-2,-77,148,-39,-35,]),'SEMICOLON':([9,33,45,54,55,56,57,63,64,65,68,69,71,72,73,91,92,96,99,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,127,133,134,135,138,],[-38,37,76,-70,-72,-33,-34,100,-40,102,-71,-73,-41,-42,-22,120,121,-70,130,131,-75,-76,132,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-74,-23,140,-36,143,]),'ASSIGNMENT':([9,45,54,55,56,57,64,68,69,71,72,73,91,96,103,104,106,107,108,109,110,111,112,113,114,115,116,117,127,133,135,],[-38,77,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,119,-70,-75,-76,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-74,-23,-36,]),'PLUS':([9,45,54,55,56,57,64,68,69,71,72,73,95,96,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,127,129,133,134,135,138,],[-38,78,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,78,-70,78,-75,78,78,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,78,78,78,78,-74,78,-23,78,-36,78,]),'MINUS':([9,45,54,55,56,57,64,68,69,71,72,73,95,96,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,127,129,133,134,135,138,],[-38,79,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,79,-70,79,-75,79,79,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,79,79,79,79,-74,79,-23,79,-36,79,]),'DIVIDE':([9,45,54,55,56,57,64,68,69,71,72,73,95,96,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,127,129,133,134,135,138,],[-38,81,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,81,-70,81,-75,81,81,81,81,-9,-10,-11,-12,-13,-14,-15,-16,-17,81,81,81,81,-74,81,-23,81,-36,81,]),'MOD':([9,45,54,55,56,57,64,68,69,71,72,73,95,96,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,127,129,133,134,135,138,],[-38,82,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,82,-70,82,-75,82,82,82,82,-9,-10,-11,-12,-13,-14,-15,-16,-17,82,82,82,82,-74,82,-23,82,-36,82,]),'LEQ':([9,45,54,55,56,57,64,68,69,71,72,73,95,96,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,127,129,133,134,135,138,],[-38,83,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,83,-70,83,83,83,83,83,83,83,83,83,-12,-13,-14,-15,-16,-17,83,83,83,83,-74,83,-23,83,-36,83,]),'GEQ':([9,45,54,55,56,57,64,68,69,71,72,73,95,96,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,127,129,133,134,135,138,],[-38,84,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,84,-70,84,84,84,84,84,84,84,84,84,-12,-13,-14,-15,-16,-17,84,84,84,84,-74,84,-23,84,-36,84,]),'LT':([9,45,54,55,56,57,64,68,69,71,72,73,95,96,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,127,129,133,134,135,138,],[-38,85,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,85,-70,85,85,85,85,85,85,85,85,85,-12,-13,-14,-15,-16,-17,85,85,85,85,-74,85,-23,85,-36,85,]),'GT':([9,45,54,55,56,57,64,68,69,71,72,73,95,96,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,127,129,133,134,135,138,],[-38,86,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,86,-70,86,86,86,86,86,86,86,86,86,-12,-13,-14,-15,-16,-17,86,86,86,86,-74,86,-23,86,-36,86,]),'EQ':([9,45,54,55,56,57,64,68,69,71,72,73,95,96,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,127,129,133,134,135,138,],[-38,87,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,87,-70,87,87,87,87,87,87,87,87,87,-12,-13,-14,-15,-16,-17,87,87,87,87,-74,87,-23,87,-36,87,]),'NE':([9,45,54,55,56,57,64,68,69,71,72,73,95,96,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,127,129,133,134,135,138,],[-38,88,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,88,-70,88,88,88,88,88,88,88,88,88,-12,-13,-14,-15,-16,-17,88,88,88,88,-74,88,-23,88,-36,88,]),'DOT':([9,45,54,55,56,57,64,68,69,71,72,73,95,96,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,127,129,133,134,135,138,],[-38,89,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,89,-70,89,-75,89,89,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,89,89,89,89,-74,89,-23,89,-36,89,]),'LBRACKET':([9,45,54,55,56,57,64,68,69,71,72,73,95,96,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,127,129,133,134,135,138,],[-38,90,-70,-72,-33,-34,-40,-71,-73,-41,-42,-22,90,-70,90,-75,90,90,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,90,90,90,90,-74,90,-23,90,-36,90,]),'IF':([9,35,39,41,42,43,44,46,47,48,49,50,51,52,55,56,57,60,64,66,68,69,71,72,73,74,76,96,97,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,120,121,127,130,131,132,133,135,140,143,144,147,149,],[-38,58,58,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,-72,-33,-34,-21,-40,-19,-71,-73,-41,-42,-22,-20,-55,-70,58,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-29,-28,-74,-24,-49,-5,-23,-36,-27,58,-77,-39,-35,]),'FOR':([9,35,39,41,42,43,44,46,47,48,49,50,51,52,55,56,57,60,64,66,68,69,71,72,73,74,76,96,97,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,120,121,127,130,131,132,133,135,140,143,144,147,149,],[-38,61,61,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,-72,-33,-34,-21,-40,-19,-71,-73,-41,-42,-22,-20,-55,-70,61,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-29,-28,-74,-24,-49,-5,-23,-36,-27,61,-77,-39,-35,]),'WHILE':([9,35,39,41,42,43,44,46,47,48,49,50,51,52,55,56,57,60,64,66,68,69,71,72,73,74,76,96,97,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,120,121,127,130,131,132,133,135,140,143,144,147,149,],[-38,62,62,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,-72,-33,-34,-21,-40,-19,-71,-73,-41,-42,-22,-20,-55,-70,62,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-29,-28,-74,-24,-49,-5,-23,-36,-27,62,-77,-39,-35,]),'BREAK':([9,35,39,41,42,43,44,46,47,48,49,50,51,52,55,56,57,60,64,66,68,69,71,72,73,74,76,96,97,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,120,121,127,130,131,132,133,135,140,143,144,147,149,],[-38,63,63,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,-72,-33,-34,-21,-40,-19,-71,-73,-41,-42,-22,-20,-55,-70,63,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-29,-28,-74,-24,-49,-5,-23,-36,-27,63,-77,-39,-35,]),'RETURN':([9,35,39,41,42,43,44,46,47,48,49,50,51,52,55,56,57,60,64,66,68,69,71,72,73,74,76,96,97,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,120,121,127,130,131,132,133,135,140,143,144,147,149,],[-38,65,65,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,-72,-33,-34,-21,-40,-19,-71,-73,-41,-42,-22,-20,-55,-70,65,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-29,-28,-74,-24,-49,-5,-23,-36,-27,65,-77,-39,-35,]),';':([9,35,39,41,42,43,44,46,47,48,49,50,51,52,55,56,57,60,64,66,68,69,71,72,73,74,76,96,97,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,120,121,127,130,131,132,133,135,140,143,144,147,149,],[-38,66,66,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,-72,-33,-34,-21,-40,-19,-71,-73,-41,-42,-22,-20,-55,-70,66,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-29,-28,-74,-24,-49,-5,-23,-36,-27,66,-77,-39,-35,]),'AMPERSAND':([9,35,39,41,42,43,44,46,47,48,49,50,51,52,55,56,57,59,60,64,65,66,67,68,69,70,71,72,73,74,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,96,97,98,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,119,120,121,127,128,130,131,132,133,135,136,140,143,144,147,149,],[-38,70,70,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,-72,-33,-34,70,-21,-40,70,-19,70,-71,-73,70,-41,-42,-22,-20,-55,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,-70,70,70,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,70,-29,-28,-74,70,-24,-49,-5,-23,-36,70,-27,70,-77,-39,-35,]),'INTL':([9,35,39,41,42,43,44,46,47,48,49,50,51,52,55,56,57,59,60,63,64,65,66,67,68,69,70,71,72,73,74,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,96,97,98,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,119,120,121,127,128,130,131,132,133,135,136,140,143,144,147,149,],[-38,64,64,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,-72,-33,-34,64,-21,99,-40,64,-19,64,-71,-73,64,-41,-42,-22,-20,-55,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,-70,64,64,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,64,-29,-28,-74,64,-24,-49,-5,-23,-36,64,-27,64,-77,-39,-35,]),'BOOLL':([9,35,39,41,42,43,44,46,47,48,49,50,51,52,55,56,57,59,60,64,65,66,67,68,69,70,71,72,73,74,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,96,97,98,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,119,120,121,127,128,130,131,132,133,135,136,140,143,144,147,149,],[-38,73,73,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,-72,-33,-34,73,-21,-40,73,-19,73,-71,-73,73,-41,-42,-22,-20,-55,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,-70,73,73,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,73,-29,-28,-74,73,-24,-49,-5,-23,-36,73,-27,73,-77,-39,-35,]),'RBRACE':([9,19,24,25,26,32,35,37,38,39,40,41,42,43,44,46,47,48,49,50,51,52,55,56,57,60,64,66,68,69,71,72,73,74,75,76,96,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,120,121,127,130,131,132,133,135,140,144,147,149,],[-38,-78,31,-78,-68,-67,-78,-66,74,-78,-64,-51,-52,-53,-54,-56,-57,-58,-59,-60,-61,-62,-72,-33,-34,-21,-40,-19,-71,-73,-41,-42,-22,-20,-63,-55,-70,-25,-50,-75,-76,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-29,-28,-74,-24,-49,-5,-23,-36,-27,-77,-39,-35,]),'RBRACKET':([9,55,56,57,64,68,69,71,72,73,96,103,104,106,107,108,109,110,111,112,113,114,115,116,117,118,127,133,135,],[-38,-72,-33,-34,-40,-71,-73,-41,-42,-22,-70,-75,-76,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,133,-74,-23,-36,]),'ELSE':([74,142,],[-20,145,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'CompilationUnit':([0,],[1,]),'DefinitionListR':([0,3,4,],[2,10,11,]),'FunctionDefinition':([0,3,4,],[3,3,3,]),'StructDefinition':([0,3,4,],[4,4,4,]),'empty':([0,3,4,7,14,17,19,25,30,35,39,54,93,136,],[5,5,5,15,15,23,26,26,23,40,40,15,124,124,]),'Type':([0,3,4,17,19,25,30,35,39,97,143,],[6,6,6,20,27,27,20,53,53,53,53,]),'Id':([0,3,4,6,8,17,19,20,25,27,30,35,39,53,59,65,67,70,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,97,98,119,128,136,143,],[7,7,7,12,16,7,7,28,7,33,7,54,54,91,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,96,54,96,96,96,96,54,]),'PointerListR':([7,14,54,],[13,18,13,]),'ParameterListR':([17,30,],[21,36,]),'Parameter':([17,30,],[22,22,]),'StructMemberListR':([19,25,],[24,32,]),'StructMember':([19,25,],[25,25,]),'Block':([29,35,39,97,137,139,143,145,148,],[34,60,60,60,142,144,60,147,149,]),'StatementListR':([35,39,],[38,75,]),'Statement':([35,39,97,143,],[39,39,128,146,]),'AssignmentStatement':([35,39,97,143,],[41,41,41,41,]),'DeclarationAssignmentStatement':([35,39,97,143,],[42,42,42,42,]),'DeclarationFunctionCallStatement':([35,39,97,143,],[43,43,43,43,]),'DeclarationStatement':([35,39,97,143,],[44,44,44,44,]),'Expression':([35,39,59,65,67,70,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,97,98,119,128,136,143,],[45,45,95,101,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,125,126,45,129,134,138,125,45,]),'IfElseStatement':([35,39,97,143,],[46,46,46,46,]),'ForStatement':([35,39,97,143,],[47,47,47,47,]),'WhileStatement':([35,39,97,143,],[48,48,48,48,]),'BreakStatement':([35,39,97,143,],[49,49,49,49,]),'ReturnStatement':([35,39,97,143,],[50,50,50,50,]),'BlockStatement':([35,39,97,143,],[51,51,51,51,]),'BlankStatement':([35,39,97,143,],[52,52,52,52,]),'FunctionCall':([35,39,53,59,65,67,70,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,97,98,119,128,136,143,],[55,55,92,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,55,]),'BinaryExpression':([35,39,59,65,67,70,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,97,98,119,128,136,143,],[56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,]),'UnaryExpression':([35,39,59,65,67,70,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,97,98,119,128,136,143,],[57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,]),'Literal':([35,39,59,65,67,70,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,97,98,119,128,136,143,],[68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,]),'BracketCall':([35,39,59,65,67,70,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,97,98,119,128,136,143,],[69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,]),'IntLiteral':([35,39,59,65,67,70,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,97,98,119,128,136,143,],[71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,]),'BoolLiteral':([35,39,59,65,67,70,77,78,79,80,81,82,83,84,85,86,87,88,89,90,93,94,97,98,119,128,136,143,],[72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,]),'ArgumentListR':([93,136,],[122,141,]),'Argument':([93,136,],[123,123,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> CompilationUnit","S'",1,None,None,None),
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
  ('BinaryExpression -> Expression DOT Expression','BinaryExpression',3,"p_<class 'parser_rules.BinaryExpression'>",'parser.py',39),
  ('BlankStatement -> ;','BlankStatement',1,"p_<class 'parser_rules.BlankStatement'>",'parser.py',28),
  ('Block -> LBRACE StatementListR RBRACE','Block',3,"p_<class 'parser_rules.Block'>",'parser.py',28),
  ('BlockStatement -> Block','BlockStatement',1,"p_<class 'parser_rules.BlockStatement'>",'parser.py',28),
  ('BoolLiteral -> BOOLL','BoolLiteral',1,"p_<class 'parser_rules.BoolLiteral'>",'parser.py',28),
  ('BracketCall -> Expression LBRACKET Expression RBRACKET','BracketCall',4,"p_<class 'parser_rules.BracketCall'>",'parser.py',28),
  ('BreakStatement -> BREAK INTL SEMICOLON','BreakStatement',3,"p_<class 'parser_rules.BreakStatement'>",'parser.py',28),
  ('BreakStatement -> BREAK SEMICOLON','BreakStatement',2,"p_<class 'parser_rules.BreakStatement'>",'parser.py',29),
  ('CompilationUnit -> DefinitionListR','CompilationUnit',1,"p_<class 'parser_rules.CompilationUnit'>",'parser.py',28),
  ('DeclarationAssignmentStatement -> Type Id ASSIGNMENT Expression SEMICOLON','DeclarationAssignmentStatement',5,"p_<class 'parser_rules.DeclarationAssignmentStatement'>",'parser.py',28),
  ('DeclarationFunctionCallStatement -> Type FunctionCall SEMICOLON','DeclarationFunctionCallStatement',3,"p_<class 'parser_rules.DeclarationFunctionCallStatement'>",'parser.py',28),
  ('DeclarationStatement -> Type Id SEMICOLON','DeclarationStatement',3,"p_<class 'parser_rules.DeclarationStatement'>",'parser.py',28),
  ('DefinitionListR -> FunctionDefinition DefinitionListR','DefinitionListR',2,"p_<class 'parser_rules.DefinitionListR'>",'parser.py',28),
  ('DefinitionListR -> StructDefinition DefinitionListR','DefinitionListR',2,"p_<class 'parser_rules.DefinitionListR'>",'parser.py',29),
  ('DefinitionListR -> empty','DefinitionListR',1,"p_<class 'parser_rules.DefinitionListR'>",'parser.py',30),
  ('Expression -> BinaryExpression','Expression',1,"p_<class 'parser_rules.Expression'>",'parser.py',28),
  ('Expression -> UnaryExpression','Expression',1,"p_<class 'parser_rules.Expression'>",'parser.py',29),
  ('ForStatement -> FOR LPAREN Statement Expression SEMICOLON Statement RPAREN Block','ForStatement',8,"p_<class 'parser_rules.ForStatement'>",'parser.py',28),
  ('FunctionCall -> Id LPAREN ArgumentListR RPAREN','FunctionCall',4,"p_<class 'parser_rules.FunctionCall'>",'parser.py',28),
  ('FunctionDefinition -> Type Id LPAREN ParameterListR RPAREN Block','FunctionDefinition',6,"p_<class 'parser_rules.FunctionDefinition'>",'parser.py',28),
  ('Id -> ID','Id',1,"p_<class 'parser_rules.Id'>",'parser.py',28),
  ('IfElseStatement -> IF LPAREN Expression RPAREN Block ELSE Block','IfElseStatement',7,"p_<class 'parser_rules.IfElseStatement'>",'parser.py',28),
  ('IntLiteral -> INTL','IntLiteral',1,"p_<class 'parser_rules.IntLiteral'>",'parser.py',28),
  ('Literal -> IntLiteral','Literal',1,"p_<class 'parser_rules.Literal'>",'parser.py',28),
  ('Literal -> BoolLiteral','Literal',1,"p_<class 'parser_rules.Literal'>",'parser.py',29),
  ('Parameter -> Type Id','Parameter',2,"p_<class 'parser_rules.Parameter'>",'parser.py',28),
  ('ParameterListR -> Parameter COMMA ParameterListR','ParameterListR',3,"p_<class 'parser_rules.ParameterListR'>",'parser.py',28),
  ('ParameterListR -> Parameter','ParameterListR',1,"p_<class 'parser_rules.ParameterListR'>",'parser.py',29),
  ('ParameterListR -> empty','ParameterListR',1,"p_<class 'parser_rules.ParameterListR'>",'parser.py',30),
  ('PointerListR -> TIMES PointerListR','PointerListR',2,"p_<class 'parser_rules.PointerListR'>",'parser.py',28),
  ('PointerListR -> empty','PointerListR',1,"p_<class 'parser_rules.PointerListR'>",'parser.py',29),
  ('ReturnStatement -> RETURN Expression SEMICOLON','ReturnStatement',3,"p_<class 'parser_rules.ReturnStatement'>",'parser.py',28),
  ('ReturnStatement -> RETURN SEMICOLON','ReturnStatement',2,"p_<class 'parser_rules.ReturnStatement'>",'parser.py',29),
  ('Statement -> AssignmentStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',28),
  ('Statement -> DeclarationAssignmentStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',29),
  ('Statement -> DeclarationFunctionCallStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',30),
  ('Statement -> DeclarationStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',31),
  ('Statement -> Expression SEMICOLON','Statement',2,"p_<class 'parser_rules.Statement'>",'parser.py',32),
  ('Statement -> IfElseStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',33),
  ('Statement -> ForStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',34),
  ('Statement -> WhileStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',35),
  ('Statement -> BreakStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',36),
  ('Statement -> ReturnStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',37),
  ('Statement -> BlockStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',38),
  ('Statement -> BlankStatement','Statement',1,"p_<class 'parser_rules.Statement'>",'parser.py',39),
  ('StatementListR -> Statement StatementListR','StatementListR',2,"p_<class 'parser_rules.StatementListR'>",'parser.py',28),
  ('StatementListR -> empty','StatementListR',1,"p_<class 'parser_rules.StatementListR'>",'parser.py',29),
  ('StructDefinition -> STRUCT Id LBRACE StructMemberListR RBRACE','StructDefinition',5,"p_<class 'parser_rules.StructDefinition'>",'parser.py',28),
  ('StructMember -> Type Id SEMICOLON','StructMember',3,"p_<class 'parser_rules.StructMember'>",'parser.py',28),
  ('StructMemberListR -> StructMember StructMemberListR','StructMemberListR',2,"p_<class 'parser_rules.StructMemberListR'>",'parser.py',28),
  ('StructMemberListR -> empty','StructMemberListR',1,"p_<class 'parser_rules.StructMemberListR'>",'parser.py',29),
  ('Type -> Id PointerListR','Type',2,"p_<class 'parser_rules.Type'>",'parser.py',28),
  ('UnaryExpression -> Id','UnaryExpression',1,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',28),
  ('UnaryExpression -> Literal','UnaryExpression',1,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',29),
  ('UnaryExpression -> FunctionCall','UnaryExpression',1,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',30),
  ('UnaryExpression -> BracketCall','UnaryExpression',1,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',31),
  ('UnaryExpression -> LPAREN Expression RPAREN','UnaryExpression',3,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',32),
  ('UnaryExpression -> TIMES Expression','UnaryExpression',2,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',33),
  ('UnaryExpression -> AMPERSAND Expression','UnaryExpression',2,"p_<class 'parser_rules.UnaryExpression'>",'parser.py',34),
  ('WhileStatement -> WHILE LPAREN Expression RPAREN Block','WhileStatement',5,"p_<class 'parser_rules.WhileStatement'>",'parser.py',28),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',35),
]
