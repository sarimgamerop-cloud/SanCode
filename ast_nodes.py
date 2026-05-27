class NumberNode:
    def __init__(self,number):
        self.number = number.token_value
    def __repr__(self):
        return f"(Number {self.number})"

class UnaryOpNode:
    def __init__(self,op,value):
        self.op = op 
        self.value = value
    def __repr__(self):
        return f"(UnaryOp{self.op} {self.value})"
    
class BinaryOpNode:
    def __init__(self,left,op,right):
        self.left = left
        self.op = op 
        self.right = right
    def __repr__(self):
        return f"(BinaryOp {self.left} {self.op} {self.right})"

class BooleanLiteral:
    def __init__(self,value):
        self.value = value
    def __repr__(self):
        return f"(BOOL {self.value})"

class VarAssignNode():
    def __init__(self, var_name_token, value_node,is_const):
        self.var_name_token = var_name_token 
        self.value_node = value_node
        self.is_const = is_const

    def __repr__(self):
        keyword = "CONST" if self.is_const else "DEC"
        return f"({keyword} {self.var_name_token.token_value} = {self.value_node})"

class VarAccessNode():
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token

    def __repr__(self):
        return f"(ACCESS {self.var_name_token.token_value})"

