const_variables = []
dec_variables = []

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

class StringLiteral:
    def __init__(self,value):
        self.value = value 
    def __repr__(self):
        return f"(STRING {self.value})"

class NullLiteral:
    def __init__(self):
        pass
    def __repr__(self):
        return f"(Null)"

class VarAssignNode():
    def __init__(self, var_name_token, value_node,is_const):
        self.var_name_token = var_name_token 
        self.value_node = value_node
        self.is_const = is_const

        if self.is_const:
            const_variables.append(var_name_token.token_value)
        else:
            dec_variables.append(var_name_token.token_value)

    def __repr__(self):
        keyword = "CONST" if self.is_const else "DEC"
        return f"({keyword} {self.var_name_token.token_value} = {self.value_node})"

class VarReassignNode:
    def __init__(self,var_name_token,value_node):
        self.var_name_token = var_name_token
        self.value_node = value_node
    def __repr__(self):
        return f"(REASSIGN {self.var_name_token} = {self.value_node})"

class VarAccessNode():
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token

    def __repr__(self):
        return f"(ACCESS {self.var_name_token.token_value})"

class BlockNode:
    def __init__(self,statements):
        self.statements = statements
    def __repr__(self):
        return f"(BLOCK {self.statements})"

class ProgramNode:
    def __init__(self,statements):
        self.statements = statements 
    def __repr__(self):
        return f"(PROGRAM {self.statements})"

class IfNode:
    def __init__(self,condition,if_body,else_body=None):
        self.condition = condition 
        self.if_body = if_body
        self.else_body = else_body
    def __repr__(self):
        if self.else_body:
            return f"(IF {self.condition} THEN {self.if_body} ELSE {self.else_body})"
        else:
            return f"(IF {self.condition} THEN {self.if_body})"

class WhileNode:
    def __init__(self,condition,while_body):
        self.condition = condition
        self.while_body = while_body
    def __repr__(self):
        return f"(WHILE {self.condition} DO {self.while_body})"

class FuncDefNode:
    def __init__(self, func_name, func_params, func_body):
        self.func_name = func_name
        self.func_params = func_params
        self.func_body = func_body
    def __repr__(self):
        func_params_names = ", ".join([parameter.token_value for parameter in self.func_params])
        return f"(DEF FUNC {self.func_name} ({func_params_names}) -> {self.func_body})"

class FuncCallNode:
    def __init__(self, func_name, func_args):
        self.func_name = func_name
        self.func_args = func_args
    def __repr__(self):
        return f"(CALL {self.func_name}({self.func_args}))"
        
class ReturnNode:
    def __init__(self,value=None):
        self.value = value
    def __repr__(self):
        return f"(RETURN {self.value})"

class BreakNode:
    def __init__(self):
        pass
    def __repr__(self):
        return f"(BREAK)"

class StdOutNode:
    def __init__(self,value_node):
        self.value_node = value_node
    def __repr__(self):
        return f"(STDOUT {self.value_node})"

class ScanNode:
    def __init__(self,variable):
        self.variable = variable
    def __repr__(self):
        return f"(SCAN {self.variable})"



