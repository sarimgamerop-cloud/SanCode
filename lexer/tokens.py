#---tokens.py-------------------------------------------------------
# This file contains all the defined tokens for the "Arc" language.
# Not to be changed further. 
#-------------------------------------------------------------------


#---Token Types----------------------------------------------------
#The definitions are categorised based on their type
#------------------------------------------------------------------

#---Data Type Tokens----------------------------------------------
TT_INT = "INTEGER"
TT_FLOAT = "FLOAT"
TT_BOOL = "BOOLEAN"
TT_STR = "STRING"
TT_NUll = "NULL"

#---Arithmetic Operators--------------------------------------------
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_SLASH = "SLASH"
TT_STAR = "STAR"

#---Membership Operators-----------------------------------------------
TT_IN = "IN"

#---Logical Operators------------------------------------------------
TT_AND = "AND"
TT_OR = "OR"
TT_NOT = "NOT"

#---Comparison Operators---------------------------------------------------
TT_GT = "GT"
TT_LT = "LT"
TT_EQ = "EQ"
TT_GTE = "GTE"
TT_LTE = "LTE"
TT_BANG = "BANG"
TT_BANGEQ = "BANGEQ"

#---Multi-char Tokens-----------------------------------------------
TT_EQEQ = "EQEQ"
TT_STARSTAR = "STARSTAR"

#---Delimiters----------------------------------------------------------
TT_DOT = "DOT"
TT_COLON = "COLON"
TT_SEMICOLON = "SEMICOLON"
TT_COMMA = "COMMA"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LBRACE = "LBRACE"
TT_RBRACE = "RBRACE"
TT_LBRACKET = "LBRACKET"
TT_RBRACKET = "RBRACKET"

#---Others---------------------------------------------------------------
TT_IDENT = "IDENT"
TT_KEYWORD = "KEYWORD"
TT_EOF = "EOF"

#---Keywords-------------------------------------------------------------
KEYWORDS = {
    'dec', 'const', 'func', 'return',
    'if', 'else', 'elif',
    'loop', 'for', 'in', 'break', 'skip',
    'out', 'prompt',
    'true', 'false', 'null',
    'use', 'type', 'init', 'ext',
    'try', 'catch', 'drop'
}

class Tokens:
    def __init__(self,token_type,line: int,column,token_value = None):
        self.token_type = token_type
        self.token_value = token_value 
        self.line = line
        self.column = column

    def __repr__(self):
        if self.token_value:
            return f"Token({self.token_type}:{self.token_value} - ln,{self.line})"
        else:
            return f"Token({self.token_type} -> ln,{self.line})"