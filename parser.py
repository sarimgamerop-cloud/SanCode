from ast_nodes import *
from scanner import *

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens 
        self.pos = 0
        self.current_token = self.tokens[0] if self.tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            None 
    
    def peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos+1]
        else:
            return None 
    
    def match(self,token_types):
        return self.current_token.type_ in token_types