class Environment:
    def __init__(self,parent=None):
        self.parent = parent
        self.vars = {}

    def define(self,name,value,is_const=False):
        if name in self.vars:
            raise Exception("Variable already exists")
        else:
            self.vars[name] = (value, is_const)
    
    def lookup(self,name):
        if name in self.vars:
            return self.vars[name][0]
        if self.parent:
            return self.parent.lookup(name)
        else:
            raise Exception("Variable not found")
    
    def reassign_var(self,name,value):
        if name in self.vars:
            val, is_const = self.vars[name]
            if is_const:
                raise Exception("Cannot flux a constant")
            else:
                self.vars[name] = (value,is_const)
                return 
            
        elif self.parent:
            self.parent.reassign_var(name,value)
            return 
        
        else:
            raise Exception("Undefined variable")


class Evaluator:
    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
    
    def evaluate(self,node):
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self,method_name,None)
        if visitor is None:
            raise Exception("No visitor node for this")
        return visitor(node)
    
    def visit_ProgramNode(self,node):
        result = None
        for statement in node.statements:
            result = self.evaluate(statement)
        return result

    def is_truthy(self,operand):
        if operand is None or operand is False:
            return False
        if operand == 0:
            return False
        else:
            return True

    def visit_NumberNode(self,node):
        if '.' in node.number:
            return float(node.number)
        else:
            return int(node.number)
    
    def visit_StringLiteral(self,node):
        return node.value
    
    def visit_BooleanLiteral(self,node):
        return node.value
    
    def visit_NullLiteral(self,node):
        return None 
    
    def visit_UnaryOpNode(self,node):
        operand = self.evaluate(node.value)

        if node.op == "+" or node.op == "":
            return +operand
        elif node.op == "-":
            return -operand
        elif node.op == "!":
            return not self.is_truthy(operand)
    
    def visit_BinaryOpNode(self,node):
        left = self.evaluate(node.left)
        operator = node.op
        right = self.evaluate(node.right)

        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right != 0:
                return left / right
            else:
                raise Exception('Zero divison error')
        elif operator == '**':
            return left ** right
        elif operator == '>':
            return left > right
        elif operator == '<':
            return left < right
        elif operator == '<=':
            return left <= right
        elif operator == '>=':
            return left >= right
        elif operator == '==':
            return left == right
        elif operator == '!=':
            return left != right
        elif operator == '&&':
            return self.is_truthy(left) and self.is_truthy(right)
        elif operator == '||':
            return self.is_truthy(left) or self.is_truthy(right)
        else:
            raise Exception(f"Unknown binary operator: {node.op}")
    
    def visit_VarAccessNode(self,node):
        return self.current_env.lookup(node.var_name_token.token_value)
    
    def visit_VarAssignNode(self,node):
        name = node.var_name_token.token_value
        value = self.evaluate(node.value_node)
        self.current_env.define(name,value,node.is_const)
        return value
    
    def visit_VarReassignNode(self,node):
        name = node.var_name_token.token_value
        value = self.evaluate(node.value_node)
        self.current_env.reassign_var(name,value)
        return value

