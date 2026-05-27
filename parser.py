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
            self.current_token = self.tokens[self.pos]
        else:
            None 
    
    def peek(self):
        if (self.pos + 1) < (len(self.tokens)):
            return self.tokens[self.pos+1]
        else:
            return None 
    
    def match(self,token_types):
        return self.current_token.type_ in token_types
    
    def expect(self,token_types):
        if self.match(token_types):
            tok = self.current_token
            self.advance()
            return tok 
        else:
            raise Exception("Unexpected token found!!")
    
    def parse_factor(self):
        if self.match([TT_PLUS,TT_MINUS,TT_BANG]):
            op = self.current_token.token_value
            self.advance()
            node = self.parse_factor()
            return UnaryOpNode(op,node)
        
        elif self.match([TT_INT,TT_FLOAT]):
            tok = self.expect([TT_INT,TT_FLOAT])
            return NumberNode(tok)
        
        elif self.match([TT_BOOL]):
            value = self.current_token.token_value
            self.advance()
            return BooleanLiteral(value)
        
        elif self.match([TT_LPAREN]):
            self.expect([TT_LPAREN])
            expression_node = self.parse_expr()
            self.expect([TT_RPAREN])
            return expression_node
        
        elif self.match([TT_IDENT]):
            variable = self.expect([TT_IDENT])
            return VarAccessNode(variable)
    
    def parse_power(self):
        left = self.parse_factor()
        if self.current_token and self.match([TT_STARSTAR]):
            op = self.current_token.token_value
            self.advance()
            right = self.parse_power()
            left = BinaryOpNode(left,op,right)
        return left
        
    def parse_term(self):
        left = self.parse_power()
        while self.current_token and self.match([TT_STAR,TT_SLASH]):
            op = self.current_token.token_value 
            self.advance()
            right = self.parse_power()
            right = right
            left = BinaryOpNode(left,op,right)
        return left 

    def parse_expr(self):
        left = self.parse_term()
        while self.current_token and self.match([TT_PLUS,TT_MINUS]):
            op = self.current_token.token_value
            self.advance()
            right = self.parse_term()
            left = BinaryOpNode(left,op,right)
        return left

    def parse_comp_expr(self):
        left = self.parse_expr()
        while self.current_token and self.match([TT_GT,TT_GTE,TT_LT,TT_LTE,TT_EQEQ,TT_BANGEQ]):
            op = self.current_token.token_value
            self.advance()
            right = self.parse_expr()
            left = BinaryOpNode(left,op,right)
        return left
    
    def parse_statements(self):
        if self.current_token and self.current_token.token_value in ('dec','const'):
            is_const = (self.current_token.token_value == 'const')
            self.expect([self.current_token.type_])
            var_name_token = self.expect([TT_IDENT])
            self.expect([TT_EQ])
            var_value_node = self.parse_comp_expr()
            return VarAssignNode(var_name_token,var_value_node,is_const)

