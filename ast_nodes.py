class BinaryOpNode:
    def __init__(self,left,op,right):
        self.left = left 
        self.op = op 
        self.right = right 
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.op} {self.right})"

class NumberNode:
    def __init__(self,op,number):
        self.number = number 
    def __repr__(self):
        return f"Number({self.op} {self.number})"