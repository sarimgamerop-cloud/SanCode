from ast_nodes import *
from scanner import *

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens 
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            None
    
    def eat(self,token_type):
        tok = self.current_token()
        if tok.type_ != token_type:
            raise Exception("Unexpected token!!")
        else:
            self.pos += 1 
            return tok 
    
    def parse_expression(self):
        left = self.parse_primary()
        tok = self.current_token()
        while tok.type_ in (TT_PLUS,TT_MINUS):
            op = self.eat(tok.type_)
            right = self.parse_primary()
            left = BinaryOpNode(left,op,right)
            return left
            

    def parse_primary(self):
        tok = self.current_token()
        if tok.type_ == TT_INT:
            self.eat(TT_INT)
            return NumberNode(tok.token_value)
        else:
            raise Exception("Unmatched token type!!")

    