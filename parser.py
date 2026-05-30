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
            self.current_token = None
    
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
            raise Exception(f"Unexpected Tokens!!! {self.current_token}")
    
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
        
        elif self.match([TT_STR]):
            value = self.current_token.token_value
            self.advance()
            return StringLiteral(value)
        
        elif self.match([TT_LPAREN]):
            self.expect([TT_LPAREN])
            expression_node = self.parse_expr()
            self.expect([TT_RPAREN])
            return expression_node
        
        elif self.current_token and self.current_token.token_value == 'Null':
            self.advance()
            return NullLiteral()

        elif self.current_token and self.current_token.token_value == 'flux':
            self.advance()
            var = self.current_token.token_value
            if (var not in const_variables):
                if (var in dec_variables):    
                    self.expect([TT_IDENT])
                    self.expect([TT_EQ])
                    value = self.parse_comp_expr()
                    return VarReassignNode(var,value)
                else:
                    raise Exception("Error!!! VAR is not declared, cant reassign")
            else:
                raise Exception("Error! Const is immutable")
            
        elif self.match([TT_IDENT]):
            variable = self.expect([TT_IDENT])
            
            if self.current_token and self.current_token.type_ == TT_LPAREN:
                self.expect([TT_LPAREN]) 
                
                args = []
                if self.current_token and self.current_token.type_ != TT_RPAREN:

                    args.append(self.parse_comp_expr())

                    while self.current_token and self.current_token.type_ == TT_COMMA:
                        self.expect([TT_COMMA])
                        args.append(self.parse_comp_expr())
                        
                self.expect([TT_RPAREN]) 
                return FuncCallNode(variable, args)
            
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
            if var_name_token.token_value not in const_variables and var_name_token.token_value not in dec_variables:
                self.expect([TT_EQ])
                var_value_node = self.parse_comp_expr()
                return VarAssignNode(var_name_token,var_value_node,is_const)
            else:
                raise Exception("Variable is already declared!!")
        
        elif self.current_token and self.current_token.token_value == 'if':
            self.expect([self.current_token.type_])
            self.expect([TT_LPAREN])
            condition = self.parse_comp_expr()
            self.expect([TT_RPAREN])
            if_body = self.parse_blocks()
            else_body = None 
            if self.current_token and self.current_token.token_value == 'else':
                self.expect([self.current_token.type_])
                else_body = self.parse_blocks()
            return IfNode(condition,if_body,else_body)
        
        elif self.current_token and self.current_token.token_value == 'while':
            self.expect([self.current_token.type_])
            self.expect([TT_LPAREN])
            condition = self.parse_comp_expr()
            self.expect([TT_RPAREN])
            while_body = self.parse_blocks()
            return WhileNode(condition,while_body)
        
        elif self.current_token and self.current_token.token_value == 'func':
            self.expect([self.current_token.type_])
            func_name = self.current_token.token_value
            self.expect([TT_IDENT])
            self.expect([TT_LPAREN])
            params = []
            if self.current_token and self.current_token.type_ != TT_RPAREN:
                params.append(self.expect([TT_IDENT]))
                while self.current_token and self.current_token.type_ == TT_COMMA:
                    self.expect([TT_COMMA])
                    params.append(self.expect([TT_IDENT]))  
            self.expect([TT_RPAREN])
            func_body = self.parse_blocks()
            return FuncDefNode(func_name,params,func_body)
        
        elif self.current_token and self.current_token.token_value == 'return':
            self.expect([self.current_token.type_])
            value = None
            if self.current_token and self.current_token.type_ not in (TT_EOF,TT_RBRACE):
                value = self.parse_comp_expr()
            return ReturnNode(value)

        elif self.current_token and self.current_token.token_value == 'break':
            self.advance()
            return BreakNode()
        
        elif self.current_token and self.current_token.token_value == 'stdout':
            self.expect([self.current_token.type_])
            self.expect([TT_LPAREN])
            value = self.parse_comp_expr()
            self.expect([TT_RPAREN])
            return StdOutNode(value)
        
        elif self.current_token and self.current_token.token_value == 'scan':
            self.expect([self.current_token.type_])
            self.expect(TT_LPAREN)
            variable = self.current_token.token_value
            self.expect([TT_IDENT])
            self.expect([TT_RPAREN])
            return ScanNode(variable)
        
        else:
            expr = self.parse_comp_expr()
            return expr
    
    def parse_statements_list(self):
        statements = []
        while self.current_token and self.current_token.type_ != TT_RBRACE:
            stmt = self.parse_statements()
            if stmt:
                statements.append(stmt)
        return statements

    def parse_blocks(self):
        if self.current_token and self.current_token.type_ == TT_LBRACE:
                self.expect([TT_LBRACE])
                statements = self.parse_statements_list()
                self.expect([TT_RBRACE])
                return statements

    def parse(self):
        statements = []
        while self.current_token.type_ != TT_EOF or self.current_token is None:
            stmt = self.parse_statements()
            if stmt:
                statements.append(stmt)
        return ProgramNode(statements)


