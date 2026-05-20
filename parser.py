from ast_nodes import *
from scanner import *

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens 
        self.pos = 0
        self.current_tok = None 
    
    def 